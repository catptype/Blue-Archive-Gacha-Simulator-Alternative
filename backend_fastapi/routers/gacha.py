import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List

from ..config import settings
from ..util.auth import get_optional_current_user
from ..util.cache import get_cache, Cache
from ..util.database import get_db
from ..util.models import GachaBanner, GachaTransaction, User, Achievement, UserInventory, Student
from ..util.schemas.AchievementResponse import AchievementResponse
from ..util.schemas.BannerResponse import BannerCacheSchema
from ..util.schemas.GachaResponse import GachaPullResponse, GachaStudentSchema
from ..util.schemas.StudentResponse import create_student_response
from ..util.AchievementEngine import AchievementEngine
from ..util.GachaEngine import GachaEngine

LOGGER = logging.getLogger(__name__)

router = APIRouter()

# --- Helper Functions ---

def _serialize_gacha_student(student_list: List[Student], banner: GachaBanner, request: Request) -> List[GachaStudentSchema]:
    pickup_ids = [s.id for s in banner.pickup_students]

    results = []
    for student in student_list:
        student_response = create_student_response(student, request)
        result_student = GachaStudentSchema(
            student=student_response,
            is_pickup=student.id in pickup_ids,
            is_new=False
        )
        results.append(result_student)

    return results

def _check_achievement(
    result_schema: List[GachaStudentSchema],
    request: Request,
    db: Session, 
    current_user: User, 
) -> List[AchievementResponse]:
    # Get the user's total pull count *before* this pull for milestone checks.
    initial_pull_count = db.query(func.count(GachaTransaction.id)).filter_by(user_id=current_user.id).scalar() or 0

    # Get number of current pull
    amount = len(result_schema)
    
    # Instantiate the achievement engine. It loads the user's existing unlocks.
    ach_engine = AchievementEngine(user=current_user, db=db)

    # Check achievement (Raw data)
    achievement_list: List[Achievement] = []
    achievement_list.extend(ach_engine.check_luck_achievements(result_schema))
    achievement_list.extend(ach_engine.check_milestone_achievements(initial_pull_count, amount))
    achievement_list.extend(ach_engine.check_collection_achievements())

    # Convert raw data to schema and save database
    achievements_response: List[AchievementResponse] = []
    for ach in achievement_list:
        
        # Convert schema
        ach_resp = AchievementResponse.model_validate(ach)
        ach_resp.image_url = str(request.url_for('serve_achievement_image', achievement_id=ach.id)) if ach.image_data else None
        achievements_response.append(ach_resp)
        
        # Preparing save database
        db.add(ach)

    # Save database
    db.commit()

    return achievements_response

def _insert_transaction(
    pulled_results: List[GachaStudentSchema],
    banner: GachaBanner,
    db: Session, 
    current_user: User, 
    cache: Cache
) -> None:

    # Pre-fetch the user's existing inventory for the pulled students to check for "new".
    pulled_student_ids = [result.student.id for result in pulled_results]
    user_inventory_query = db.query(UserInventory).filter(
        UserInventory.user_id == current_user.id,
        UserInventory.student_id.in_(pulled_student_ids)
    )

    # Create a dictionary for fast lookups: {student_id: UserInventory_obj}
    inventory_map = {item.student_id: item for item in user_inventory_query}

    # Process pull result for labeling "new" or "pickup"
    for result in pulled_results:
        student = result.student

        # Create a transaction record for each pulled student.
        new_transaction = GachaTransaction(
            user_id=current_user.id,
            banner_id=banner.id,
            student_id=student.id
        )
        db.add(new_transaction)

        # Update is_new value for GachaStudentSchema in user mode
        result.is_new = student.id not in inventory_map

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

    # Commit database
    db.commit()

    # Clear dashboard cache for this user
    cache_pattern = f"dashboard:*:{current_user.id}*"
    cache.delete_by_pattern(cache_pattern)

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

    cache_key = f"gacha:banner:{banner_id}"
    banner_data = cache.get(cache_key)

    if banner_data:
        LOGGER.debug(f"Banner '{banner_id}' hit cache.")
        # Deserialize JSON back into the Pydantic Schema
        banner = BannerCacheSchema.model_validate(banner_data)

    else:
        LOGGER.debug(f"Banner '{banner_id}' missed cache. Fetching from DB.")
        banner_db = db.query(GachaBanner).filter_by(id=banner_id).first()

        if not banner_db:
            raise HTTPException(status_code=404, detail="Banner not found")

        # Convert SQLAlchemy object to Pydantic Schema
        banner = BannerCacheSchema.model_validate(banner_db)
        
        # Save to cache
        cache.set(cache_key, banner.model_dump(mode='json'), expire=settings.CACHE_EXPIRE)
    
    # Perform gacha pulling
    engine = GachaEngine(banner=banner, db=db) # banner must be GachaBanner
    student_list = engine.draw(amount)

    # Create GachaStudentSchema
    result_schema = _serialize_gacha_student(student_list, banner, request)

    # Return response pulling result immediately
    if current_user is None:
        LOGGER.debug("Guest is pulling. Skipping transaction history.")
        
        return GachaPullResponse(
            results=result_schema,
            unlocked_achievements=[]
        )

    # Perform saving transaction and achievement database before response
    LOGGER.debug(f"User '{current_user.username}' is pulling. Processing inventory and transactions...")
    _insert_transaction(result_schema, banner, db, current_user, cache)
    unlocked_achievements = _check_achievement(result_schema, request, db, current_user)
    
    # --- Format the final response, including any unlocked achievements ---
    return GachaPullResponse(
        results=result_schema,
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