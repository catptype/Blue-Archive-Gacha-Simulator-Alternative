import random
from typing import List
from decimal import Decimal
from sqlalchemy.orm import Session
from . import models

class GachaEngine:
    """
    A stateless service class that handles the logic of performing gacha pulls,
    including a 10-pull guarantee system. Works with SQLAlchemy models.
    """
    def __init__(self, banner: models.GachaBanner, db: Session):
        if not banner.preset:
            raise ValueError("Banner does not have a rate preset.")

        self.banner = banner

        # --- 1. Calculate rates from the preset ---
        self.rates = {
            "r3": banner.preset.preset_r3_rate,
            "r2": banner.preset.preset_r2_rate,
            "r1": banner.preset.preset_r1_rate
        }
        # This is the rate for non-pickup 3-stars
        self.non_pickup_r3_rate = self.rates["r3"] - banner.preset.preset_pickup_rate

        # --- 2. Build the student pools using SQLAlchemy ---
        # Get IDs needed for filtering
        pickup_ids = {s.student_id for s in banner.pickup_students}
        excluded_ids = {s.student_id for s in banner.excluded_students}
        included_version_ids = {v.version_id for v in banner.included_versions}

        # Build the base query for the general pool
        base_pool_query = db.query(models.Student).filter(
            models.Student.version_id_fk.in_(included_version_ids),
            models.Student.student_id.not_in(pickup_ids | excluded_ids)
        )
        if not banner.banner_include_limited:
            base_pool_query = base_pool_query.filter(models.Student.student_is_limited == False)

        # Execute query once and partition in Python for efficiency
        all_pool_students = base_pool_query.all()

        self.pools = {
            "pickup": banner.pickup_students,
            "r3": [s for s in all_pool_students if s.student_rarity == 3],
            "r2": [s for s in all_pool_students if s.student_rarity == 2],
            "r1": [s for s in all_pool_students if s.student_rarity == 1],
        }

        # --- 3. Calculate rates and weights for the guaranteed pull ---
        self.guaranteed_r2_rates = {
            "r3": self.rates["r3"],
            "r2": self.rates["r2"] + self.rates["r1"] # R1 rate is absorbed by R2
        }

        # --- 4. Pre-calculate weights for each pool ---
        self.weights = {
            "pickup": [banner.preset.preset_pickup_rate / len(self.pools["pickup"])] * len(self.pools["pickup"]) if self.pools["pickup"] else [],
            "r3": [self.non_pickup_r3_rate / len(self.pools["r3"])] * len(self.pools["r3"]) if self.pools["r3"] else [],
            "r2": [self.rates["r2"] / len(self.pools["r2"])] * len(self.pools["r2"]) if self.pools["r2"] else [],
            "r1": [self.rates["r1"] / len(self.pools["r1"])] * len(self.pools["r1"]) if self.pools["r1"] else [],
        }
    
    def _draw_one(self, *, guarantee_r2_or_higher: bool = False) -> models.Student:
        """Internal helper to perform a single pull. Returns a single SQLAlchemy Student object."""
        active_rates = self.guaranteed_r2_rates if guarantee_r2_or_higher else self.rates
        
        # Layer 1: Determine Rarity
        chosen_rarity = random.choices(
            population=list(active_rates.keys()), 
            weights=[float(w) for w in active_rates.values()], # Ensure weights are floats
            k=1
        )[0]

        # Layer 2: Choose a student from the corresponding pool
        if chosen_rarity == "r3":
            combined_r3_pool = self.pools["pickup"] + self.pools["r3"]
            combined_r3_weights = self.weights["pickup"] + self.weights["r3"]
            if not combined_r3_pool: # Fallback if 3-star pool is empty
                return random.choice(self.pools["r2"]) if self.pools["r2"] else random.choice(self.pools["r1"])
            return random.choices(combined_r3_pool, weights=[float(w) for w in combined_r3_weights], k=1)[0]
        
        elif chosen_rarity == "r2":
            if not self.pools["r2"]: # Fallback
                return random.choice(self.pools["r1"]) if not guarantee_r2_or_higher else self._draw_one(guarantee_r2_or_higher=True)
            return random.choices(self.pools["r2"], weights=[float(w) for w in self.weights["r2"]], k=1)[0]
            
        elif chosen_rarity == "r1": # Only reachable on a normal pull
            if not self.pools["r1"]: # Should be very rare
                raise Exception("Gacha Error: R1 Pool is empty.")
            return random.choices(self.pools["r1"], weights=[float(w) for w in self.weights["r1"]], k=1)[0]

    def draw(self, amount: int) -> List[models.Student]:
        """Performs a pull of a specified amount, handling 10-pull guarantees."""
        if amount == 10:
            # 9 r1~r3 pulls + 1 guaranteed r2+ pull
            pulled_students = [self._draw_one() for _ in range(9)]
            guaranteed_pull = self._draw_one(guarantee_r2_or_higher=True)
            pulled_students.append(guaranteed_pull)
            return pulled_students
        elif amount == 1:
            return [self._draw_one()]
        else:
            raise ValueError("Pull amount must be 1 or 10.")
        
