import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List, Tuple

from ..util.auth import get_optional_current_user
from ..util.cache import get_cache, Cache
from ..util.database import get_db
from ..util.models import GachaBanner, GachaTransaction, User, Achievement, UserInventory, Student
from ..util.schemas.AchievementResponse import AchievementResponse
from ..util.schemas.GachaResponse import GachaPullResponse, GachaResultStudent
from ..util.schemas.StudentResponse import create_student_response
from ..util.AchievementEngine import AchievementEngine
from ..util.GachaEngine import GachaEngine

LOGGER = logging.getLogger(__name__)

router = APIRouter()

# --- Helper Functions ---

def _serialize_gacha_result(student: Student, request: Request, pickup_id_list:list, is_new:bool=False) -> GachaResultStudent:
    student_response = create_student_response(student, request)
    result_student = GachaResultStudent(
        **student_response.model_dump(),
        is_pickup=(student.id in pickup_id_list),
        is_new=is_new
    )
    return result_student

def _insert_transaction(
    amount: int,
    banner: GachaBanner,
    pulled_results: List[Student], 
    db: Session, 
    request: Request,
    current_user: User, 
    cache: Cache
) -> Tuple[List[GachaResultStudent], List[AchievementResponse]]:
    
    # Prepare pickup student id
    pickup_ids = {s.id for s in banner.pickup_students}

    # Get the user's total pull count *before* this pull for milestone checks.
    initial_pull_count = db.query(func.count(GachaTransaction.id)).filter_by(user_id=current_user.id).scalar() or 0

    # Instantiate the achievement engine. It loads the user's existing unlocks.
    ach_engine = AchievementEngine(user=current_user, db=db)

    # Pre-fetch the user's existing inventory for the pulled students to check for "new".
    pulled_student_ids = [s.id for s in pulled_results]
    user_inventory_query = db.query(UserInventory).filter(
        UserInventory.user_id == current_user.id,
        UserInventory.student_id.in_(pulled_student_ids)
    )

    # Create a dictionary for fast lookups: {student_id: UserInventory_obj}
    inventory_map = {item.student_id: item for item in user_inventory_query}

    # Process pull result for labeling "new" or "pickup"
    final_results: List[GachaResultStudent] = []
    for student in pulled_results:

        # Create a transaction record for each pulled student.
        new_transaction = GachaTransaction(
            user_id=current_user.id,
            banner_id=banner.id,
            student_id=student.id
        )
        db.add(new_transaction)

        # Check if this student is new for the user's inventory.
        is_new = student.id not in inventory_map

        # Update or create the inventory entry.
        inventory_item = inventory_map.get(student.id)
        if inventory_item:
            inventory_item.num_obtained += 1
        else:
            new_inventory_item = UserInventory(
                user_id=current_user.id,
                student_id=student.id,
                num_obtained=1
            )
            db.add(new_inventory_item)
            inventory_map[student.id] = new_inventory_item
        
        # Build the decorated result object for the frontend response.
        result_student = _serialize_gacha_result(student, request, pickup_ids, is_new)
        final_results.append(result_student)

    # Check achievements
    unlocked_achievements: List[Achievement] = []
    unlocked_achievements.extend(ach_engine.check_luck_achievements(pulled_results))
    unlocked_achievements.extend(ach_engine.check_milestone_achievements(initial_pull_count, amount))
    newly_unlocked_collection = ach_engine.check_collection_achievements()
    if newly_unlocked_collection:
        unlocked_achievements.extend(newly_unlocked_collection)

    # Commit database
    db.commit()

    # Clear dashboard cache for this user
    cache_pattern = f"dashboard:*:{current_user.id}*"
    cache.delete_by_pattern(cache_pattern)

    # Post processing for unlocked achievements
    achievements_response: List[AchievementResponse] = []
    for ach in unlocked_achievements:
        ach_resp = AchievementResponse.model_validate(ach)
        ach_resp.image_url = str(request.url_for('serve_achievement_image', achievement_id=ach.id)) if ach.image_data else None
        achievements_response.append(ach_resp)

    return final_results, achievements_response

def _perform_pull(
        banner_id: int,
        amount: int,
        db: Session,
        request: Request,
        current_user: User | None,
        cache: Cache
    ) -> GachaPullResponse:
    """
    Internal function that uses the GachaEngine and conditionally saves
    transactions based on whether a user is present.
    """
    # ... (fetching the banner and instantiating the engine is the same)
    banner = db.query(GachaBanner).options(
        joinedload(GachaBanner.preset),
        selectinload(GachaBanner.pickup_students),
        selectinload(GachaBanner.excluded_students),
        selectinload(GachaBanner.included_versions)
    ).filter_by(id=banner_id).first()
    
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    
    # Perform gacha pulling
    engine = GachaEngine(banner=banner, db=db)
    pulled_results = engine.draw(amount)

    if current_user is None:
        LOGGER.debug("Guest is pulling. Skipping transaction history.")
        
        # Prepare pickup student id
        pickup_ids = {s.id for s in banner.pickup_students}

        final_results = []
        for student in pulled_results:
            result_student = _serialize_gacha_result(student, request, pickup_ids)
            final_results.append(result_student)
        
        return GachaPullResponse(
            results=final_results,
            unlocked_achievements=[]
        )

    # Check current user for saving transaction
    LOGGER.debug(f"User '{current_user.username}' is pulling. Processing inventory and transactions...")
    final_results, unlocked_achievements = _insert_transaction(amount, banner, pulled_results, db, request, current_user, cache)
    
    # --- Format the final response, including any unlocked achievements ---
    return GachaPullResponse(
        results=final_results,
        unlocked_achievements=unlocked_achievements # Mocked for now
    )

# --- Endpoints ---

@router.post("/{banner_id}/pull_single", response_model=GachaPullResponse)
def perform_gacha_pull_single(
    banner_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
    cache: Cache = Depends(get_cache)
):
    return _perform_pull(
        banner_id=banner_id, amount=1, db=db, request=request, current_user=current_user, cache=cache
    )

@router.post("/{banner_id}/pull_ten", response_model=GachaPullResponse)
def perform_gacha_pull_ten(
    banner_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
    cache: Cache = Depends(get_cache)
):
    return _perform_pull(
        banner_id=banner_id, amount=10, db=db, request=request, current_user=current_user, cache=cache
    )