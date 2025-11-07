import base64
import hashlib

from datetime import timedelta
from fastapi import APIRouter, FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import Optional, List
from sqlalchemy import func, desc
from collections import Counter, defaultdict
from .util import auth, models, schemas
from .util.auth import get_optional_current_user, get_required_current_user
from .util.cache import get_cache, Cache
from .util.database import engine, get_db
from .util.schemas import create_student_response
from .util.GachaEngine import GachaEngine
from .util.admin import init_admin

app = FastAPI()
init_admin(app)

# --- CORS Middleware ---
origins = ["http://localhost:5173", "http://localhost:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- Helper Functions ---
def _perform_pull(
        banner_id: int,
        amount: int,
        db: Session,
        request: Request,
        current_user: models.User | None # <-- Accept the optional user object
    ) -> schemas.GachaPullResponse:
    """
    Internal function that uses the GachaEngine and conditionally saves
    transactions based on whether a user is present.
    """
    # ... (fetching the banner and instantiating the engine is the same)
    banner = db.query(models.GachaBanner).options(
        joinedload(models.GachaBanner.preset),
        selectinload(models.GachaBanner.pickup_students),
        selectinload(models.GachaBanner.excluded_students),
        selectinload(models.GachaBanner.included_versions)
    ).filter(models.GachaBanner.banner_id == banner_id).first()
    
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    
    engine = GachaEngine(banner=banner, db=db)
    pulled_students_orm = engine.draw(amount)

    # Initialize variables for the response
    pickup_ids = {s.student_id for s in banner.pickup_students}
    final_results: List[schemas.GachaResultStudent] = []

    # --- THIS IS THE KEY CHANGE ---
    # Only try to save transactions if a user object was provided.
    if current_user:
        print(f"User '{current_user.username}' is pulling. Processing inventory and transactions...")

        # A) EFFICIENTLY PRE-FETCH the user's existing inventory for the pulled students.
        # This avoids querying the database inside the loop (prevents N+1 problem).
        pulled_student_ids = [s.student_id for s in pulled_students_orm]
        user_inventory_query = db.query(models.UserInventory).filter(
            models.UserInventory.user_id_fk == current_user.user_id,
            models.UserInventory.student_id_fk.in_(pulled_student_ids)
        )
        # Create a dictionary for fast lookups: {student_id: UserInventory_object}
        inventory_map = {item.student_id_fk: item for item in user_inventory_query}

        # B) LOOP through the gacha results to process each one.
        for student in pulled_students_orm:

            # i. Create a transaction record for every pull.
            new_transaction = models.GachaTransaction(
                user_id_fk=current_user.user_id,
                banner_id_fk=banner_id,
                student_id_fk=student.student_id
            )
            db.add(new_transaction)

            # ii. Check if this is a new student FOR THE USER.
            # This is determined by looking at the inventory state *before* this pull started.
            is_new = student.student_id not in inventory_map

            # iii. Update or create the inventory entry.
            inventory_item = inventory_map.get(student.student_id)
            if inventory_item:
                # The user already has this student, so just increment the count.
                inventory_item.inventory_num_obtained += 1
            else:
                # This is the first time the user has ever obtained this student.
                # Create a new inventory record.
                new_inventory_item = models.UserInventory(
                    user_id_fk=current_user.user_id,
                    student_id_fk=student.student_id,
                    inventory_num_obtained=1
                )
                db.add(new_inventory_item)
                # IMPORTANT: Add the newly created item to our map. This correctly
                # handles the case where the user pulls the same *new* student
                # multiple times in a single 10-pull. The first one will be marked
                # as `is_new=True`, and the second one will be found here and incremented.
                inventory_map[student.student_id] = new_inventory_item
            
            # iv. Build the decorated result for the frontend response.
            student_response = create_student_response(student, request)
            result_student = schemas.GachaResultStudent(
                **student_response.model_dump(),
                is_pickup=(student.student_id in pickup_ids),
                is_new=is_new
            )
            final_results.append(result_student)

        # C) COMMIT all changes (new transactions, new/updated inventory) at once.
        db.commit()
    else:
        print("Guest is pulling. Skipping transaction history.")
        for student in pulled_students_orm:
            student_response = create_student_response(student, request)
            result_student = schemas.GachaResultStudent(
                **student_response.model_dump(),
                is_pickup=(student.student_id in pickup_ids),
                is_new=False # Guests never have "new" students
            )
            final_results.append(result_student)
    # --- END OF CHANGE ---
    
    # 4. Return an instance of the main response schema
    return schemas.GachaPullResponse(
        success=True,
        results=final_results,
        unlocked_achievements=[] # Mocked for now
    )

# --- Authentication Endpoints ---

@app.post("/api/register/", response_model=schemas.UserSchema)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # --- START OF CHANGES ---
    # Fetch the default role object from the database.
    member_role = db.query(models.Role).filter(models.Role.role_name == "member").first()
    if not member_role:
        # This is a critical server error, the 'member' role should always exist.
        raise HTTPException(status_code=500, detail="Default user role not configured on server.")

    hashed_password = auth.get_password_hash(user.password)
    
    new_user = models.User(
        username=user.username, 
        hashed_password=hashed_password,
        role_id_fk=member_role.role_id  # Assign the foreign key ID
    )
    # --- END OF CHANGES ---

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=schemas.UserSchema)
def read_users_me(current_user: models.User = Depends(get_required_current_user)):
    """
    Fetches the data for the currently authenticated user.
    If the token is invalid or expired, this endpoint will automatically
    return a 401 Unauthorized error.
    """
    return current_user

@app.post("/api/admin/clear-cache", status_code=204)
def clear_all_caches(cache: Cache = Depends(get_cache)):
    cache_key_list = ["all_schools"]
    for key in cache_key_list:
        cache.delete(key)
        print(f"CACHE CLEARED for {key}")
    return None

# --- API Endpoints ---

@app.get("/api/banners/", response_model=list[schemas.BannerResponse])
def get_banners(request: Request, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):
    cache_key = "all_banners"

    response_banners = cache.get(cache_key)
    if response_banners:
        print(f"CACHE HIT ({cache_key})")
        return response_banners

    print(f"CACHE MISS ({cache_key})")
    db_banners = db.query(models.GachaBanner).all()

    response_banners = []
    for banner in db_banners:
        banner_data = schemas.BannerResponse.model_validate(banner)
        if banner.banner_image:
            banner_data.image_url = str(request.url_for('serve_banner_image', banner_id=banner.banner_id))
        response_banners.append(banner_data)

    banners_to_cache = [b.dict() for b in response_banners]
    cache.set(cache_key, banners_to_cache, expire=300)
        
    return response_banners
    

@app.get("/api/schools/", response_model=list[schemas.SchoolResponse])
def get_schools(request: Request, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):
    cache_key = "all_schools"

    response_schools = cache.get(cache_key)
    if response_schools:
        print(f"CACHE HIT ({cache_key})")
        return response_schools
    
    print(f"CACHE MISS ({cache_key})")
    db_schools = db.query(models.School).all()
    
    response_schools = []
    for school in db_schools:
        school_data = schemas.SchoolResponse.model_validate(school)
        if school.school_image:
            school_data.image_url = str(request.url_for('serve_school_image', school_id=school.school_id))
        response_schools.append(school_data)

    schools_to_cache = [s.dict() for s in response_schools]
    cache.set(cache_key, schools_to_cache, expire=300)
        
    return response_schools

@app.get("/api/students/", response_model=list[schemas.StudentResponse])
def get_students(
        request: Request, 
        school_id: Optional[int] = None,
        version_id: Optional[int] = None,
        db: Session = Depends(get_db)
    ):
    
    # Start with a base query
    students_query = (
        db.query(models.Student)
        .options(joinedload(models.Student.school), joinedload(models.Student.version), joinedload(models.Student.asset))
    )
    
    # If a school_id was provided in the URL, apply the filter
    if school_id is not None:
        students_query = students_query.filter(models.Student.school_id_fk == school_id)

    if version_id is not None:
        students_query = students_query.filter(models.Student.version_id_fk == version_id)

    db_students = students_query.all()
    
    response_students = []
    for student in db_students:
        # Step 1: Validate the base student and its nested school object
        student_response = schemas.StudentResponse.model_validate(student)

        # Step 2: Create the school response object, adding the URL
        school_response = schemas.SchoolResponse.model_validate(student.school)
        if student.school.school_image:
             school_response.image_url = str(request.url_for('serve_school_image', school_id=student.school.school_id))

        student_response.portrait_url = str(request.url_for('serve_student_image', student_id=student.student_id, image_type='portrait'))
        student_response.artwork_url = str(request.url_for('serve_student_image', student_id=student.student_id, image_type='artwork'))
        
        response_students.append(student_response)
        
    return response_students

@app.get("/api/banners/{banner_id}/details/", response_model=schemas.BannerDetailResponse)
def get_banner_details(banner_id: int, request: Request, db: Session = Depends(get_db)):
    # 1. Fetching logic is unchanged.
    db_banner = db.query(models.GachaBanner).options(
        joinedload(models.GachaBanner.preset),
        selectinload(models.GachaBanner.pickup_students).options(
            joinedload(models.Student.school), joinedload(models.Student.version), joinedload(models.Student.asset)
        ),
        selectinload(models.GachaBanner.included_versions),
        selectinload(models.GachaBanner.excluded_students)
    ).filter(models.GachaBanner.banner_id == banner_id).first()

    if not db_banner:
        raise HTTPException(status_code=404, detail="Banner not found")

    # 2. & 3. Querying and partitioning logic is also unchanged.
    pickup_ids = {s.student_id for s in db_banner.pickup_students}
    excluded_ids = {s.student_id for s in db_banner.excluded_students}
    included_version_ids = {v.version_id for v in db_banner.included_versions}

    base_pool_query = db.query(models.Student).options(
        joinedload(models.Student.school), joinedload(models.Student.version), joinedload(models.Student.asset)
    ).filter(
        models.Student.version_id_fk.in_(included_version_ids),
        models.Student.student_id.not_in(pickup_ids | excluded_ids)
    )

    if not db_banner.banner_include_limited:
        base_pool_query = base_pool_query.filter(models.Student.student_is_limited == False)

    all_pool_students_db = base_pool_query.all()

    nonpickup_r3_students_db = [s for s in all_pool_students_db if s.student_rarity == 3]
    r2_students_db = [s for s in all_pool_students_db if s.student_rarity == 2]
    r1_students_db = [s for s in all_pool_students_db if s.student_rarity == 1]
    
    pickup_r3_students_db = [s for s in db_banner.pickup_students if s.student_rarity == 3]

    # --- 4. ASSEMBLE THE RESPONSE (The Updated Part) ---

    # Step 4a: Create the base banner data using the BannerResponse schema
    # This automatically handles banner_id, banner_name, and the nested preset.
    base_banner_response = schemas.BannerResponse.model_validate(db_banner)
    
    # Step 4b: Manually add the computed image_url
    base_banner_response.image_url = str(request.url_for('serve_banner_image', banner_id=db_banner.banner_id)) if db_banner.banner_image else None

    # Step 4c: Convert all the partitioned student lists to the correct response schema
    pickup_r3_response = [create_student_response(s, request) for s in pickup_r3_students_db]
    nonpickup_r3_response = [create_student_response(s, request) for s in nonpickup_r3_students_db]
    r2_response = [create_student_response(s, request) for s in r2_students_db]
    r1_response = [create_student_response(s, request) for s in r1_students_db]

    # Step 4d: Construct the final BannerDetailResponse
    # We unpack the base response and add the student lists.
    # Pydantic's `model_dump()` is the new way to get a dict from a model instance.
    final_response = schemas.BannerDetailResponse(
        **base_banner_response.model_dump(),
        pickup_r3_students=pickup_r3_response,
        nonpickup_r3_students=nonpickup_r3_response,
        r2_students=r2_response,
        r1_students=r1_response
    )

    return final_response

# --- UPDATE the pull endpoints to use the new dependency ---
@app.post("/api/gacha/{banner_id}/pull_single", response_model=schemas.GachaPullResponse)
def perform_gacha_pull_single(
    banner_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User | None = Depends(get_optional_current_user) # Inject optional user
):
    return _perform_pull(
        banner_id=banner_id, amount=1, db=db, request=request, current_user=current_user
    )

@app.post("/api/gacha/{banner_id}/pull_ten", response_model=schemas.GachaPullResponse)
def perform_gacha_pull_ten(
    banner_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User | None = Depends(get_optional_current_user) # Inject optional user
):
    return _perform_pull(
        banner_id=banner_id, amount=10, db=db, request=request, current_user=current_user
    )

@app.get("/api/dashboard/summary/kpis", response_model=schemas.DashboardKpiResponse)
def get_dashboard_kpis(
    current_user: models.User = Depends(get_required_current_user),
    db: Session = Depends(get_db)
):
    # --- PERFORMANCE IMPROVEMENT: Fetch all rarities in a single, efficient query ---
    rarity_pulls = db.query(models.Student.student_rarity).join(
        models.GachaTransaction, models.GachaTransaction.student_id_fk == models.Student.student_id
    ).filter(
        models.GachaTransaction.user_id_fk == current_user.user_id
    ).all()

    # The result is a list of tuples, e.g., [(3,), (2,), (2,)].
    # We use a Counter to efficiently count them.
    rarity_counter = Counter(r[0] for r in rarity_pulls)
    total_pulls = len(rarity_pulls)

    # Return an instance of the Pydantic schema
    return schemas.DashboardKpiResponse(
        total_pulls=total_pulls,
        total_pyroxene_spent=total_pulls * 120,
        r3_count=rarity_counter.get(3, 0),
        r2_count=rarity_counter.get(2, 0),
        r1_count=rarity_counter.get(1, 0),
    )

@app.get("/api/dashboard/summary/top-students/{rarity}", response_model=List[schemas.TopStudentResponse])
def get_top_students_by_rarity(
    rarity: int,
    request: Request, # Add Request to build image URLs
    current_user: models.User = Depends(get_required_current_user),
    db: Session = Depends(get_db), 
    cache: Cache = Depends(get_cache)
):
    
    cache_key = f"dashboard:top_students:{current_user.user_id}:{rarity}"

    # 3. Try to get the data from the cache first
    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"CACHE HIT for {cache_key}")
        # The data in the cache is already a JSON-serializable list of dicts.
        # FastAPI will automatically validate it against the response_model.
        return cached_data
    
    print(f"CACHE MISS for {cache_key}")
    
    # The database query is unchanged
    top_students_query = (
        db.query(
            models.Student,
            func.count(models.Student.student_id).label('count'),
            func.min(models.GachaTransaction.transaction_create_on).label('first_obtained')
        )
        .join(models.GachaTransaction)
        .filter(
            models.GachaTransaction.user_id_fk == current_user.user_id,
            models.Student.student_rarity == rarity
        )
        .group_by(models.Student.student_id)
        .order_by(func.count(models.Student.student_id).desc(), func.min(models.GachaTransaction.transaction_create_on).asc())
        .limit(3)
        .all()
    )
    
    # --- BUILD THE SCHEMA RESPONSE ---
    response_data: List[schemas.TopStudentResponse] = []
    for student_orm, count, first_obtained in top_students_query:
        # 1. Reuse our helper to create the detailed StudentResponse
        student_response = create_student_response(student_orm, request)
        
        # 2. Create an instance of our new TopStudentResponse schema
        entry = schemas.TopStudentResponse(
            student=student_response,
            count=count,
            first_obtained=first_obtained
        )
        response_data.append(entry)

    data_to_cache = [entry.model_dump(mode="json") for entry in response_data]
    cache.set(cache_key, data_to_cache, expire=300) # Cache for 1 hour
        
    return response_data

@app.get(
    "/api/dashboard/summary/first-r3-pull", 
    response_model=Optional[schemas.GachaTransactionResponse] # The response can be null
)
def get_first_r3_pull(
    request: Request,
    current_user: models.User = Depends(get_required_current_user),
    db: Session = Depends(get_db),
    cache: Cache = Depends(get_cache)
):
    """
    Finds the user's first-ever 3-star pull transaction.
    """
    cache_key = f"dashboard:first_r3_pull:{current_user.user_id}"
    
    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"CACHE HIT for {cache_key}")
        # The special value "NONE" indicates a cached "not found" result
        return None if cached_data == "NONE" else cached_data

    print(f"CACHE MISS for {cache_key}")
    first_r3_pull_orm = (
        db.query(models.GachaTransaction)
        .join(models.Student)
        .filter(
            models.GachaTransaction.user_id_fk == current_user.user_id,
            models.Student.student_rarity == 3
        )
        .order_by(models.GachaTransaction.transaction_create_on.asc())
        .first()
    )

    if not first_r3_pull_orm:
        # Cache the "not found" result for 1 hour to prevent re-querying
        cache.set(cache_key, "NONE", expire=3600)
        return None

    # Build the Pydantic response object
    student_response = create_student_response(first_r3_pull_orm.student, request)
    response_data = schemas.GachaTransactionResponse(
        transaction_id=first_r3_pull_orm.transaction_id,
        transaction_create_on=first_r3_pull_orm.transaction_create_on,
        student=student_response
    )
    
    # Cache the successful result
    cache.set(cache_key, response_data.model_dump(mode="json"), expire=None) # Cache forever

    return response_data

@app.get(
    "/api/dashboard/summary/chart-overall-rarity", 
    response_model=schemas.OverallRarityChartResponse
)
def get_chart_overall_rarity(
    current_user: models.User = Depends(get_required_current_user),
    db: Session = Depends(get_db),
    cache: Cache = Depends(get_cache)
):
    cache_key = f"dashboard:chart_overall_rarity:{current_user.user_id}"
    
    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"CACHE HIT for {cache_key}")
        return cached_data

    print(f"CACHE MISS for {cache_key}")
    
    # Efficiently query just the rarity of all students the user has pulled
    rarity_pulls = db.query(models.Student.student_rarity).join(
        models.GachaTransaction, models.GachaTransaction.student_id_fk == models.Student.student_id
    ).filter(
        models.GachaTransaction.user_id_fk == current_user.user_id
    ).all()
    
    # The result is a list of tuples like [(3,), (2,), (2,)]. Use Counter to count them.
    rarity_counter = Counter(r[0] for r in rarity_pulls)
    
    response_data = schemas.OverallRarityChartResponse(
        r3_count=rarity_counter.get(3, 0),
        r2_count=rarity_counter.get(2, 0),
        r1_count=rarity_counter.get(1, 0),
    )
    
    # Cache the result for 1 hour
    cache.set(cache_key, response_data.model_dump(), expire=300)

    return response_data

@app.get(
    "/api/dashboard/summary/chart-banner-breakdown",
    response_model=schemas.BannerBreakdownChartResponse
)
def get_chart_banner_breakdown(
    current_user: models.User = Depends(get_required_current_user),
    db: Session = Depends(get_db),
    cache: Cache = Depends(get_cache)
):
    cache_key = f"dashboard:chart_banner_breakdown:{current_user.user_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"CACHE HIT for {cache_key}")
        return cached_data

    print(f"CACHE MISS for {cache_key}")
    
    # Efficiently fetch all pulls with banner name and student rarity
    pulls = db.query(
        models.GachaBanner.banner_name,
        models.Student.student_rarity
    ).join(
        models.GachaTransaction, models.GachaTransaction.banner_id_fk == models.GachaBanner.banner_id
    ).join(
        models.Student, models.GachaTransaction.student_id_fk == models.Student.student_id
    ).filter(models.GachaTransaction.user_id_fk == current_user.user_id).all()

    # Process in Python for speed
    pulls_by_banner = defaultdict(Counter)
    for banner_name, rarity in pulls:
        pulls_by_banner[banner_name][rarity] += 1
    
    response_data = {}
    for banner_name, rarity_counter in pulls_by_banner.items():
        response_data[banner_name] = schemas.OverallRarityChartResponse(
            r3_count=rarity_counter.get(3, 0),
            r2_count=rarity_counter.get(2, 0),
            r1_count=rarity_counter.get(1, 0),
        )
    
    final_response = schemas.BannerBreakdownChartResponse(data=response_data)
    cache.set(cache_key, final_response.model_dump(), expire=300)
    return final_response

# --- Image Serving Endpoints (No changes needed here) ---
@app.get("/image/banner/{banner_id}", name="serve_banner_image")
def serve_banner_image(banner_id: int, request: Request, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):

    cache_key = f"image:banner:{banner_id}"

    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"CACHE HIT for {cache_key}")
        image_bytes = base64.b64decode(cached_data['image_b64'])
        etag = cached_data['etag']
    else:
        # 3. If cache miss, query the database
        print(f"CACHE MISS for {cache_key}")
        banner = db.query(models.GachaBanner).filter(models.GachaBanner.banner_id == banner_id).first()
        if not banner or not banner.banner_image:
            raise HTTPException(status_code=404, detail="School image not found")

        image_bytes = banner.banner_image

        etag = hashlib.sha1(image_bytes).hexdigest()
        image_b64_string = base64.b64encode(image_bytes).decode("utf-8")

        data_to_cache = {
            "etag": etag,
            "image_b64": image_b64_string
        }
        # Store in the application cache for 1 hour (3600 seconds)
        cache.set(cache_key, data_to_cache, expire=3600)
    
    # 5. Check the browser's cache using the ETag
    # The browser sends this header if it has a cached version.
    if request.headers.get("if-none-match") == etag:
        print(f"CACHE HIT (Browser - 304) for {cache_key}")
        # A 304 response tells the browser to use its local copy.
        return Response(status_code=304)

    # 6. If it's a new request or the ETag doesn't match, send the full response
    # and include headers that tell the browser to cache the image.
    headers = {
        "Cache-Control": "public, max-age=86400",  # Cache for 1 day
        "ETag": etag
    }
    return Response(content=image_bytes, media_type="image/png", headers=headers)

@app.get("/image/school/{school_id}", name="serve_school_image")
def serve_school_image(school_id: int, request: Request, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):
    
    cache_key = f"image:school:{school_id}"

    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"CACHE HIT for {cache_key}")
        image_bytes = base64.b64decode(cached_data['image_b64'])
        etag = cached_data['etag']
    else:
        # 3. If cache miss, query the database
        print(f"CACHE MISS for {cache_key}")
    
        school = db.query(models.School).filter(models.School.school_id == school_id).first()
        if not school or not school.school_image:
            raise HTTPException(status_code=404, detail="School image not found")
        
        image_bytes = school.school_image

        # 4. Generate the ETag and prepare data for caching
        etag = hashlib.sha1(image_bytes).hexdigest()
        image_b64_string = base64.b64encode(image_bytes).decode("utf-8")

        data_to_cache = {
            "etag": etag,
            "image_b64": image_b64_string
        }
        # Store in the application cache for 1 hour (3600 seconds)
        cache.set(cache_key, data_to_cache, expire=3600)
    
    # 5. Check the browser's cache using the ETag
    # The browser sends this header if it has a cached version.
    if request.headers.get("if-none-match") == etag:
        print(f"CACHE HIT (Browser - 304) for {cache_key}")
        # A 304 response tells the browser to use its local copy.
        return Response(status_code=304)

    # 6. If it's a new request or the ETag doesn't match, send the full response
    # and include headers that tell the browser to cache the image.
    headers = {
        "Cache-Control": "public, max-age=86400",  # Cache for 1 day
        "ETag": etag
    }
    return Response(content=image_bytes, media_type="image/png", headers=headers)

@app.get("/image/student/{student_id}/{image_type}", name="serve_student_image")
def serve_student_image(student_id: int, image_type: str, request: Request, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):
    
    cache_key = f"image:student:{student_id}:{image_type}"

    cached_data = cache.get(cache_key)
    if cached_data:
        print(f"CACHE HIT for {cache_key}")
        # Data in cache is stored as a dictionary with etag and the b64 image
        image_bytes = base64.b64decode(cached_data['image_b64'])
        etag = cached_data['etag']
    else:
        print(f"CACHE MISS for {cache_key}")
        student = db.query(models.Student).options(joinedload(models.Student.asset)).filter(models.Student.student_id == student_id).first()

        if not student or not student.asset:
            raise HTTPException(status_code=404, detail="Student asset not found")

        image_bytes = None
        if image_type == "portrait":
            image_bytes = student.asset.asset_portrait_data
        elif image_type == "artwork":
            image_bytes = student.asset.asset_artwork_data
        
        if not image_bytes:
            raise HTTPException(status_code=404, detail="Image data not found for this type")
        
        # 4. Generate the ETag and prepare data for caching
        etag = hashlib.sha1(image_bytes).hexdigest()
        image_b64_string = base64.b64encode(image_bytes).decode("utf-8")
        
        data_to_cache = {
            "etag": etag,
            "image_b64": image_b64_string
        }
        # Store in the application cache for 1 hour
        cache.set(cache_key, data_to_cache, expire=300)
    
    # 5. Check the browser cache using the ETag
    print(request.headers.get("if-none-match"))
    if request.headers.get("if-none-match") == etag:
        print(f"CACHE HIT (Browser - 304) for {cache_key}")
        return Response(status_code=304)

    # 6. If it's a new request or the ETag doesn't match, send the full response
    # with the correct headers to enable browser caching for next time.
    headers = {
        "Cache-Control": "public, max-age=86400",  # Cache for 1 day (86400 seconds)
        "ETag": etag
    }
    return Response(content=image_bytes, media_type="image/png", headers=headers)