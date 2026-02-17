import json
import logging
from pathlib import Path
from typing import List, Optional, Set
from sqlalchemy.orm import Session
from .models import User, UserInventory, Achievement, UnlockAchievement, Student, Version
from .schemas.GachaResponse import GachaStudentSchema 

LOGGER = logging.getLogger(__name__)

# --- Load Collection Achievement Definitions at Startup ---
# This replicates your Django logic of loading JSON files once.
COLLECTION_SETS = {}
try:
    achievements_dir = Path(__file__).parent / "data" / "achievements"
    for file_path in achievements_dir.glob("*.json"):
        with open(file_path, 'r') as f:
            data = json.load(f)
            if data.get("category") == "COLLECTION" and "students" in data:
                COLLECTION_SETS[data["key"]] = data["students"]
except Exception as e:
    LOGGER.error(f"WARNING: Could not load collection achievement definitions: {e}")

class AchievementEngine:
    def __init__(self, user: User, db: Session):
        
        if not user:
            raise ValueError("A valid user is required.")
        
        self.user = user
        self.db = db

        # Fetch all unlocked achievement keys for current user.
        self.unlocked_keys: Set[str] = {
            item[0] for item in db.query(Achievement.key).join(
                UnlockAchievement, 
                UnlockAchievement.achievement_id == Achievement.id
            ).filter_by(user_id=self.user.id)
        }

    def _award(self, unlock_key: str) -> Optional[Achievement]:
        """Awards an achievement if not already unlocked."""
        if unlock_key in self.unlocked_keys:
            return None

        achievement_to_award = self.db.query(Achievement).filter_by(key=unlock_key).first()
        if not achievement_to_award:
            LOGGER.error(f"ERROR: Achievement with key '{unlock_key}' not found in DB.")
            return None
        
        new_unlock = UnlockAchievement(
            user_id=self.user.id,
            achievement_id=achievement_to_award.id
        )
        self.db.add(new_unlock)
        self.unlocked_keys.add(unlock_key) # Update in-memory set
        LOGGER.info(f"ACHIEVEMENT UNLOCKED for {self.user.username}: {achievement_to_award.name}")
        return achievement_to_award

    # --- "RULE" METHODS ---

    def check_luck_achievements(self, pulled_students: List[GachaStudentSchema]) -> List[Achievement]:
        """Checks for achievements related to a single gacha pull (e.g., multi-3-star)."""
        newly_unlocked = []
        r3_count = sum(1 for student in pulled_students if student.rarity == 3)
        
        if r3_count >= 2:
            if ach := self._award('LUCK_DOUBLE_R3'):
                newly_unlocked.append(ach)
        
        if r3_count >= 3:
            if ach := self._award('LUCK_TRIPLE_R3'):
                newly_unlocked.append(ach)
        
        return newly_unlocked

    def check_collection_achievements(self) -> List[Achievement]:
        """Checks all collection-based achievements against the user's full inventory."""
        newly_unlocked = []
        
        # Get the user's full collection for checking
        owned_students_query = (
            self.db.query(Student.name, Version.name)                       # Query student name and version columns
            .join(UserInventory, UserInventory.student_id == Student.id)    # Join table UserInventory where Userinventory has student id ...
            .join(Version, Student.version_id == Version.id)                # Join table Version where Student has version id ...
            .filter(UserInventory.user_id == self.user.id)                  # Filter UserInventory where user id ...
        )
        user_owned_set = {f"{name}|{version}" for name, version in owned_students_query}

        for unlock_key, required_students in COLLECTION_SETS.items():
            if unlock_key in self.unlocked_keys:
                continue
            
            required_set = {f"{req['name']}|{req['version']}" for req in required_students}
            if not required_set.issubset(user_owned_set):
                continue
            
            ach = self._award(unlock_key)
            if ach is not None:
                newly_unlocked.append(ach)
        
        return newly_unlocked
        
    def check_milestone_achievements(self, initial_pull_count: int, pull_amount: int) -> List[Achievement]:
        """Checks for achievements related to total pulls."""
        newly_unlocked = []
        final_pull_count = initial_pull_count + pull_amount

        # Check for milestones crossed in this pull
        if final_pull_count >= 10:
            ach = self._award('MILESTONE_PULLS_10')
            if ach is not None:
                newly_unlocked.append(ach)
        
        if final_pull_count >= 1000:
            ach = self._award('MILESTONE_PULLS_1000')
            if ach is not None:
                newly_unlocked.append(ach)
        
        return newly_unlocked