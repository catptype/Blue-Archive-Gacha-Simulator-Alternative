import logging
from collections import Counter, defaultdict
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy import func, desc, case
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List, Optional
import math
import statistics
from ..config import settings
from ..util.auth import get_required_current_user
from ..util.models import GachaBanner, GachaTransaction, User, Achievement, UserInventory, Student, GachaPreset, UnlockAchievement
from ..util.cache import get_cache, Cache
from ..util.database import get_db
from ..util.schemas.StudentResponse import create_student_response
from ..util.schemas.BannerResponse import BannerResponse
from ..util.schemas.DashboardResponse import KpiResponse, LuckGapsSchema, OverallRaritySchema, Top3StudentResponse, FirstR3Response, BannerBreakdownChartResponse, MilestoneResponse, LuckPerformanceResponse, CollectionProgressionResponse
from ..util.schemas.HistoryResponse import HistoryResponse, TransactionSchema
from ..util.schemas.CollectionResponse import CollectionResponse, CollectionStudentSchema
from ..util.schemas.AchievementResponse import UserAchievementResponse, AchievementResponse

LOGGER = logging.getLogger(__name__)

router = APIRouter()


@router.get("/summary/kpis", response_model=KpiResponse)
def get_dashboard_kpis(
    current_user: User = Depends(get_required_current_user),
    db: Session = Depends(get_db)
):
    # --- PERFORMANCE IMPROVEMENT: Fetch all rarities in a single, efficient query ---
    rarity_pulls = db.query(Student.rarity).join(
        GachaTransaction, GachaTransaction.student_id == Student.id
    ).filter(
        GachaTransaction.user_id == current_user.id
    ).all()

    # The result is a list of tuples, e.g., [(3,), (2,), (2,)].
    # We use a Counter to efficiently count them.
    rarity_counter = Counter(r[0] for r in rarity_pulls)
    total_pulls = len(rarity_pulls)

    # Return an instance of the Pydantic schema
    return KpiResponse(
        total_pulls=total_pulls,
        total_pyroxene_spent=total_pulls * 120,
        r3_count=rarity_counter.get(3, 0),
        r2_count=rarity_counter.get(2, 0),
        r1_count=rarity_counter.get(1, 0),
    )

@router.get("/summary/top-students/{rarity}", response_model=List[Top3StudentResponse])
def get_top_students_by_rarity(
    rarity: int,
    request: Request, # Add Request to build image URLs
    current_user: User = Depends(get_required_current_user),
    db: Session = Depends(get_db), 
    cache: Cache = Depends(get_cache)
):
    
    cache_key = f"dashboard:top_students:{current_user.id}:{rarity}"

    # 3. Try to get the data from the cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        LOGGER.debug(f"CACHE HIT for {cache_key}")
        # The data in the cache is already a JSON-serializable list of dicts.
        # FastAPI will automatically validate it against the response_model.
        return cached_data
    
    LOGGER.debug(f"CACHE MISS for {cache_key}")
    
     # --- START OF THE NEW, EFFICIENT QUERY ---

    # Step 1: Create a subquery that works ONLY on the GachaTransaction table.
    # It finds the most frequent student_id for this user.
    top_student_ids_subquery = (
        db.query(
            GachaTransaction.student_id,
            func.count(GachaTransaction.student_id).label('count'),
            func.min(GachaTransaction.create_on).label('first_obtained')
        )
        .join(Student) # Join to filter by rarity
        .filter(
            GachaTransaction.user_id == current_user.id,
            Student.rarity == rarity
        )
        .group_by(GachaTransaction.student_id)
        .order_by(func.count(GachaTransaction.student_id).desc(), func.min(GachaTransaction.create_on).asc())
        .limit(3)
        .subquery()
    )

    # Step 2: Join the small result of the subquery with the Student table
    # to get the full student details.
    top_students_query = (
        db.query(
            Student,
            top_student_ids_subquery.c.count,
            top_student_ids_subquery.c.first_obtained
        )
        .join(
            top_student_ids_subquery,
            Student.id == top_student_ids_subquery.c.student_id
        )
        .order_by(top_student_ids_subquery.c.count.desc(), top_student_ids_subquery.c.first_obtained.asc())
        .all()
    )
    # --- END OF THE NEW QUERY ---
    
    # --- BUILD THE SCHEMA RESPONSE ---
    response_data: List[Top3StudentResponse] = []
    for student_orm, count, first_obtained in top_students_query:
        # 1. Reuse our helper to create the detailed StudentResponse
        student_response = create_student_response(student_orm, request)
        
        # 2. Create an instance of our new TopStudentResponse schema
        entry = Top3StudentResponse(
            student=student_response,
            count=count,
            first_obtained=first_obtained
        )
        response_data.append(entry)

    data_to_cache = [entry.model_dump(mode="json") for entry in response_data]
    cache.set(cache_key, data_to_cache, expire=settings.CACHE_EXPIRE) # Cache for 1 hour
        
    return response_data

@router.get(
    "/summary/first-r3-pull", 
    response_model=Optional[FirstR3Response] # The response can be null
)
def get_first_r3_pull(
    request: Request,
    current_user: User = Depends(get_required_current_user),
    db: Session = Depends(get_db),
    cache: Cache = Depends(get_cache)
):
    """
    Finds the user's first-ever 3-star pull transaction.
    """
    cache_key = f"dashboard:first_r3_pull:{current_user.id}"
    
    cached_data = cache.get(cache_key)
    if cached_data:
        LOGGER.debug(f"CACHE HIT for {cache_key}")
        # The special value "NONE" indicates a cached "not found" result
        return None if cached_data == "NONE" else cached_data

    LOGGER.debug(f"CACHE MISS for {cache_key}")
    first_r3_pull_orm = (
        db.query(GachaTransaction)
        .join(Student)
        .filter(
            GachaTransaction.user_id == current_user.id,
            Student.rarity == 3
        )
        .order_by(GachaTransaction.create_on.asc())
        .first()
    )

    if not first_r3_pull_orm:
        # Cache the "not found" result for 1 hour to prevent re-querying
        cache.set(cache_key, "NONE", expire=settings.CACHE_EXPIRE)
        return None

    # Build the Pydantic response object
    student_response = create_student_response(first_r3_pull_orm.student, request)
    response_data = FirstR3Response(
        transaction_id=first_r3_pull_orm.transaction_id,
        transaction_create_on=first_r3_pull_orm.transaction_create_on,
        student=student_response
    )
    
    # Cache the successful result
    cache.set(cache_key, response_data.model_dump(mode="json"), expire=settings.CACHE_EXPIRE) # Cache forever

    return response_data

@router.get(
    "/summary/chart-banner-breakdown",
    response_model=BannerBreakdownChartResponse
)
def get_chart_banner_breakdown(
    current_user: User = Depends(get_required_current_user),
    db: Session = Depends(get_db),
    cache: Cache = Depends(get_cache)
):
    cache_key = f"dashboard:chart_banner_breakdown:{current_user.id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        LOGGER.debug(f"CACHE HIT for {cache_key}")
        return cached_data

    LOGGER.debug(f"CACHE MISS for {cache_key}")
    
    # Efficiently fetch all pulls with banner name and student rarity
    pulls = db.query(
        GachaBanner.name,
        Student.rarity
    ).join(
        GachaTransaction, GachaTransaction.banner_id == GachaBanner.id
    ).join(
        Student, GachaTransaction.student_id == Student.id
    ).filter(GachaTransaction.user_id == current_user.id).all()

    # Process in Python for speed
    pulls_by_banner = defaultdict(Counter)
    for banner_name, rarity in pulls:
        pulls_by_banner[banner_name][rarity] += 1
    
    response_data = {}
    for banner_name, rarity_counter in pulls_by_banner.items():
        response_data[banner_name] = OverallRaritySchema(
            r3_count=rarity_counter.get(3, 0),
            r2_count=rarity_counter.get(2, 0),
            r1_count=rarity_counter.get(1, 0),
        )
    
    final_response = BannerBreakdownChartResponse(data=response_data)
    cache.set(cache_key, final_response.model_dump(), expire=settings.CACHE_EXPIRE)
    return final_response

@router.get(
    "/summary/milestone-timeline",
    response_model=List[MilestoneResponse]
)
def get_milestone_timeline(
    request: Request,
    current_user: User = Depends(get_required_current_user),
    db: Session = Depends(get_db),
    cache: Cache = Depends(get_cache)
):
    cache_key = f"dashboard:milestones:{current_user.id}"
    cached_data = cache.get(cache_key)
    if cached_data is not None: # More robust check for any cached data
        LOGGER.debug(f"CACHE HIT for {cache_key}")
        # If the cached value is our special string, return an empty list.
        # Otherwise, return the cached data itself.
        return [] if cached_data == "NONE" else cached_data
    LOGGER.debug(f"CACHE MISS for {cache_key}")
    
    # --- START OF THE NEW, EFFICIENT QUERY ---

    # Step 1: Create a subquery (like a temporary virtual table) that numbers
    # every single pull for the current user chronologically.
    numbered_pulls_subquery = (
        db.query(
            GachaTransaction.student_id,
            func.row_number().over(order_by=GachaTransaction.create_on.asc()).label("pull_number")
        )
        .filter(GachaTransaction.user_id == current_user.id)
        .subquery()
    )

    # Step 2: Find the milestone pulls. Instead of querying the full Student object,
    # Step 2: Query from the subquery to find the *first* (minimum) pull number
    # for each unique 3-star student.
    milestone_query_results = (
        db.query(
            Student.id,
            func.min(numbered_pulls_subquery.c.pull_number).label("first_pull_number")
        )
        .join(
            numbered_pulls_subquery,
            Student.id == numbered_pulls_subquery.c.student_id
        )
        .filter(Student.rarity == 3)
        .group_by(Student.id)
        .order_by(func.min(numbered_pulls_subquery.c.pull_number).asc())
        .all()
    )

    if not milestone_query_results:
        cache.set(cache_key, "NONE", expire=settings.CACHE_EXPIRE)
        return []
    
    # Step 3: Now that we have the small list of milestone student IDs, fetch their
    # full ORM objects in a second, simple query. This query WILL correctly use `lazy='joined'`.
    milestone_student_ids = [item[0] for item in milestone_query_results]
    students_orm = db.query(Student).filter(Student.id.in_(milestone_student_ids)).all()
    
    # Create a lookup map for easy access
    student_map = {s.id: s for s in students_orm}

    # --- END OF THE NEW QUERY ---

    # 4. Process the results by combining the two query results.
    milestone_pulls: List[MilestoneResponse] = []
    for student_id, pull_number in milestone_query_results:
        student_orm = student_map.get(student_id)
        if student_orm:
            student_response = create_student_response(student_orm, request)
            milestone_entry = MilestoneResponse(
                student=student_response,
                pull_number=pull_number
            )
            milestone_pulls.append(milestone_entry)


    # 3. Process the small, final result set into the response schema.
    # The result is a list of tuples: (Student_object, pull_number)
    # milestone_pulls: List[MilestoneResponse] = []
    # for student_orm, pull_number in milestone_query_results:
    #     student_response = create_student_response(student_orm, request)
    #     milestone_entry = MilestoneResponse(
    #         student=student_response,
    #         pull_number=pull_number
    #     )
    #     milestone_pulls.append(milestone_entry)
    
    data_to_cache = [entry.model_dump(mode="json") for entry in milestone_pulls]
    cache.set(cache_key, data_to_cache, expire=settings.CACHE_EXPIRE)

    return milestone_pulls

@router.get(
    "/summary/performance-table",
    response_model=List[LuckPerformanceResponse]
)
def get_performance_table(
    current_user: User = Depends(get_required_current_user),
    db: Session = Depends(get_db),
    cache: Cache = Depends(get_cache)
):
    cache_key = f"dashboard:performance_table:{current_user.id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        LOGGER.debug(f"CACHE HIT for {cache_key}")
        return cached_data

    LOGGER.debug(f"CACHE MISS for {cache_key}")

    # 1. Perform an efficient aggregation query to get stats for ALL banners at once.
    banner_stats_query = (
        db.query(
            GachaBanner.id,
            GachaBanner.name,
            GachaPreset.r3_rate,
            func.count(GachaTransaction.id).label("total_pulls"),
            func.sum(case((Student.rarity == 3, 1), else_=0)).label("r3_count")
        )
        .join(GachaTransaction, GachaTransaction.banner_id == GachaBanner.id)
        .join(Student, GachaTransaction.student_id == Student.id)
        .join(GachaPreset, GachaBanner.preset_id == GachaPreset.id)
        .filter(GachaTransaction.user_id == current_user.id)
        .group_by(GachaBanner.id, GachaBanner.name, GachaPreset.r3_rate)
        .order_by(GachaBanner.name)
    ).all()

    banner_analysis: List[LuckPerformanceResponse] = []
    for banner_id, banner_name, banner_rate_decimal, total_pulls, r3_count in banner_stats_query:
        banner_rate = float(banner_rate_decimal)
        user_rate = (r3_count / total_pulls) * 100 if total_pulls > 0 else 0.0
        luck_variance = float(user_rate) - banner_rate # solve datatype problem if use mysql for 'decimal.Decimal' and 'float'

        gaps_data = None
        # 2. Only perform the expensive gap analysis if there are enough 3-stars.
        if r3_count > 1:
            # Fetch the chronological pulls FOR THIS BANNER ONLY.
            r3_pulls_for_banner = db.query(
                func.row_number().over(
                    order_by=GachaTransaction.create_on.asc(),
                    partition_by=GachaTransaction.banner_id
                ).label("pull_num")
            ).filter(
                GachaTransaction.user_id == current_user.id,
                GachaTransaction.banner_id == banner_id,
                GachaTransaction.student_id.in_(
                    db.query(Student.id).filter(Student.rarity == 3)
                )
            ).order_by("pull_num").all()
            
            r3_indices = [p[0] for p in r3_pulls_for_banner]
            gaps = [r3_indices[i] - r3_indices[i-1] for i in range(1, len(r3_indices))]
            
            gaps_data = LuckGapsSchema(
                min=min(gaps),
                max=max(gaps),
                avg=round(statistics.mean(gaps), 1)
            )

        # 3. Assemble the Pydantic model for this row.
        analysis_entry = LuckPerformanceResponse(
            banner_name=banner_name,
            total_pulls=total_pulls,
            r3_count=r3_count,
            user_rate=round(user_rate, 2),
            banner_rate=banner_rate,
            luck_variance=round(luck_variance, 2),
            gaps=gaps_data
        )
        banner_analysis.append(analysis_entry)

    data_to_cache = [entry.model_dump() for entry in banner_analysis]
    cache.set(cache_key, data_to_cache, expire=settings.CACHE_EXPIRE)
    
    return banner_analysis

@router.get(
    "/summary/collection-progression",
    response_model=List[CollectionProgressionResponse]
)
def get_collection_progression(
    current_user: User = Depends(get_required_current_user),
    db: Session = Depends(get_db),
    cache: Cache = Depends(get_cache)
):
    cache_key = f"dashboard:collection_progression:{current_user.id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        LOGGER.debug(f"CACHE HIT for {cache_key}")
        return cached_data

    LOGGER.debug(f"CACHE MISS for {cache_key}")

    # Query 1: Get the total number of students for each rarity.
    # This is the same for all users, so it's very fast.
    total_counts_query = (
        db.query(
            Student.rarity,
            func.count(Student.id)
        ).group_by(Student.rarity).all()
    )
    total_map = {rarity: count for rarity, count in total_counts_query}

    # Query 2: Get the number of unique students the USER has obtained for each rarity.
    obtained_counts_query = (
        db.query(
            Student.rarity,
            func.count(UserInventory.student_id)
        )
        .join(Student)
        .filter(UserInventory.user_id == current_user.id)
        .group_by(Student.rarity)
    ).all()
    obtained_map = {rarity: count for rarity, count in obtained_counts_query}

    # Assemble the response
    response_data: List[CollectionProgressionResponse] = []
    for rarity in [3, 2, 1]: # Iterate in desired display order
        obtained_count = obtained_map.get(rarity, 0)
        total_count = total_map.get(rarity, 0)
        
        response_data.append(CollectionProgressionResponse(
            rarity=rarity,
            obtained=obtained_count,
            total=total_count
        ))
        
    data_to_cache = [entry.model_dump() for entry in response_data]
    # Cache for 1 hour. This should be invalidated after a pull that yields a *new* student.
    cache.set(cache_key, data_to_cache, expire=3600)

    return response_data

@router.get("/history", response_model=HistoryResponse)
def get_user_history(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(5, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_required_current_user),
    db: Session = Depends(get_db)
):
    # 1. First, get the total count of transactions for this user (fast query)
    total_items_query = db.query(func.count(GachaTransaction.id)).filter(
        GachaTransaction.user_id == current_user.id
    )
    total_items = total_items_query.scalar()
    
    if total_items == 0:
        return HistoryResponse(
            total_items=0, total_pages=0, current_page=1, limit=limit, items=[]
        )

    # 2. Calculate total pages and offset
    total_pages = math.ceil(total_items / limit)
    offset = (page - 1) * limit

    # 3. Fetch the items for the requested page
    history_query = (
        db.query(GachaTransaction)
        .filter(GachaTransaction.user_id == current_user.id)
        .order_by(GachaTransaction.create_on.desc())
        .offset(offset)
        .limit(limit)
    )
    history_items_orm = history_query.all()

    # 4. Convert ORM objects to Pydantic schemas
    history_items_response = []
    for tx in history_items_orm:
        student_resp = create_student_response(tx.student, request)
        banner_resp = BannerResponse.model_validate(tx.banner)
        banner_resp.image_url = str(request.url_for('serve_banner_image', banner_id=tx.banner.id)) if tx.banner.image_data else None
        
        history_items_response.append(TransactionSchema(
            transaction_id=tx.id,
            transaction_create_on=tx.create_on,
            student=student_resp,
            banner=banner_resp
        ))
        
    # 5. Return the structured paginated response
    return HistoryResponse(
        total_items=total_items,
        total_pages=total_pages,
        current_page=page,
        limit=limit,
        items=history_items_response
    )

@router.get("/collection", response_model=CollectionResponse)
def get_user_collection(
    request: Request,
    current_user: User = Depends(get_required_current_user),
    db: Session = Depends(get_db),
    cache: Cache = Depends(get_cache)
):
    cache_key = f"dashboard:collection:{current_user.id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        LOGGER.debug(f"CACHE HIT for {cache_key}")
        return cached_data

    LOGGER.debug(f"CACHE MISS for {cache_key}")

    # --- START OF THE NEW, EFFICIENT QUERY ---

    # Step 1: Create a subquery containing ONLY the student IDs this user owns.
    # This is a very fast, small, temporary "virtual table".
    owned_students_subquery = (
        db.query(UserInventory.student_id)
        .filter(UserInventory.user_id == current_user.id)
        .subquery()
    )

    # Step 2: Query the main Student table and LEFT JOIN it to our subquery.
    # The result of the check `owned_students_subquery.c.student_id.isnot(None)`
    # will be our `is_obtained` boolean flag.
    all_students_with_status = (
        db.query(
            Student,
            (owned_students_subquery.c.student_id.isnot(None)).label("is_obtained")
        )
        .outerjoin( # This creates the LEFT OUTER JOIN
            owned_students_subquery,
            Student.id == owned_students_subquery.c.student_id
        )
        .options(
            joinedload(Student.school),
            joinedload(Student.version),
            joinedload(Student.asset) # Good practice to be explicit
        )
        .order_by(Student.rarity.desc(), Student.student_name.asc())
        .all()
    )

    # --- END OF THE NEW QUERY ---
    
    # 3. Process the results. The result is a list of tuples: (Student, is_obtained_boolean)
    collection_students: List[CollectionStudentSchema] = []
    obtained_count = 0
    for student_orm, is_obtained in all_students_with_status:
        if is_obtained:
            obtained_count += 1
            
        student_response = create_student_response(student_orm, request)
        collection_student = CollectionStudentSchema(
            **student_response.model_dump(),
            is_obtained=is_obtained
        )
        collection_students.append(collection_student)

    # 4. Calculate final stats
    total_students = len(all_students_with_status)
    completion_percentage = (obtained_count / total_students) * 100 if total_students > 0 else 0

    response_data = CollectionResponse(
        obtained_count=obtained_count,
        total_students=total_students,
        completion_percentage=round(completion_percentage, 2),
        students=collection_students
    )
    
    # Cache the result
    cache.set(cache_key, response_data.model_dump(mode="json"), expire=3600)
    return response_data

@router.get("/achievements", response_model=List[UserAchievementResponse])
def get_user_achievements(
    request: Request,
    current_user: User = Depends(get_required_current_user),
    db: Session = Depends(get_db),
    cache: Cache = Depends(get_cache)
):
    cache_key = f"dashboard:achievements:{current_user.id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        LOGGER.debug(f"CACHE HIT for {cache_key}")
        return cached_data
    
    LOGGER.debug(f"CACHE MISS for {cache_key}")

    # Use a LEFT JOIN to fetch all achievements and augment them with unlock data
    # for the current user in a single, efficient query.
    achievements_with_status = (
        db.query(
            Achievement,
            UnlockAchievement.unlock_on
        )
        .outerjoin(
            UnlockAchievement,
            (Achievement.id == UnlockAchievement.achievement_id) &
            (UnlockAchievement.user_id == current_user.id)
        )
        .order_by(Achievement.category, Achievement.name)
        .all()
    )

    # Process the query result into the response schema
    response_data = []
    for ach_orm, unlock_on in achievements_with_status:
        achievement_data = AchievementResponse.model_validate(ach_orm)
        achievement_data.image_url = str(request.url_for('serve_achievement_image', achievement_id=ach_orm.id)) if ach_orm.image_data else None
        
        response_data.append(UserAchievementResponse(
            **achievement_data.model_dump(),
            is_unlocked=unlock_on is not None,
            unlocked_on=unlock_on
        ))

    # Cache the result. This should be invalidated when a new achievement is unlocked.
    cache.set(cache_key, [item.model_dump(mode="json") for item in response_data], expire=3600)
    return response_data
