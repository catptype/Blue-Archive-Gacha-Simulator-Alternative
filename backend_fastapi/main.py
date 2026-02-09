import logging
import math
import statistics

from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, status, Query

from fastapi.middleware.cors import CORSMiddleware

from logging.config import dictConfig
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import Optional, List
from sqlalchemy import func, desc, case

from .log import LOGGING_CONFIG
from .util.models import School, Student
from .util.admin import init_admin

from .util.cache import get_cache, Cache
from .util.database import get_db
from .util.schemas.StudentResponse import create_student_response

from .util.schemas.SchoolResponse import SchoolResponse
from .util.schemas.StudentResponse import StudentResponse
from .util.schemas.DashboardResponse import KpiResponse, LuckGapsSchema, OverallRaritySchema, Top3StudentResponse, FirstR3Response, BannerBreakdownChartResponse, MilestoneResponse, LuckPerformanceResponse, CollectionProgressionResponse
from .util.schemas.HistoryResponse import HistoryResponse, TransactionSchema
from .util.schemas.CollectionResponse import CollectionResponse, CollectionStudentSchema
from .util.schemas.AchievementResponse import UserAchievementResponse, AchievementResponse

from .util.auth import get_optional_current_user, get_required_current_user

from .routers import users, banners, images, gacha, dashboard
from .config import settings

# `__name__` will automatically create a logger named "backend.main"
dictConfig(LOGGING_CONFIG)
LOGGER = logging.getLogger(__name__)

app = FastAPI()
api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(banners.router, prefix="/banners", tags=["banners"])
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(gacha.router, prefix="/gacha", tags=["gacha"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

# 3. Attach the Master Router to the App with the "/api" prefix
app.include_router(api_router, prefix="/api")

init_admin(app)

# --- CORS Middleware ---
origins = ["http://localhost:5173", "http://localhost:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- API Endpoints for webpage ---

@app.get("/api/schools/", tags=["web"], response_model=list[SchoolResponse])
def get_schools(request: Request, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):
    cache_key = "all_schools"

    cached_data = cache.get(cache_key)
    if cached_data:
        LOGGER.debug(f"CACHE HIT ({cache_key})")
        return [SchoolResponse.model_validate(item) for item in cached_data]
    
    LOGGER.debug(f"CACHE MISS ({cache_key})")
    db_schools = db.query(School).all()
    
    response_schools:List[SchoolResponse] = []
    for school in db_schools:
        school_data = SchoolResponse.model_validate(school)
        if school.image_data:
            school_data.image_url = str(request.url_for('serve_school_image', school_id=school.id))
        response_schools.append(school_data)

    schools_to_cache = [s.model_dump(mode='json') for s in response_schools]
    cache.set(cache_key, schools_to_cache, expire=settings.CACHE_EXPIRE)
        
    return response_schools

@app.get("/api/students/", tags=["web"], response_model=list[StudentResponse])
def get_students(
        request: Request, 
        school_id: Optional[int] = None,
        version_id: Optional[int] = None,
        db: Session = Depends(get_db)
    ):
    
    # Start with a base query
    students_query = (
        db.query(Student)
        .options(joinedload(Student.school), joinedload(Student.version), joinedload(Student.asset))
    )
    
    # If a school_id was provided in the URL, apply the filter
    if school_id is not None:
        students_query = students_query.filter(Student.school_id == school_id)

    if version_id is not None:
        students_query = students_query.filter(Student.version_id == version_id)

    db_students = students_query.all()
    
    response_students = []
    for student in db_students:
        # Step 1: Validate the base student and its nested school object
        student_response = StudentResponse.model_validate(student)

        # Step 2: Create the school response object, adding the URL
        school_response = SchoolResponse.model_validate(student.school)
        if student.school.image_data:
             school_response.image_url = str(request.url_for('serve_school_image', school_id=student.school.id))

        student_response.portrait_url = str(request.url_for('serve_student_image', student_id=student.id, image_type='portrait'))
        student_response.artwork_url = str(request.url_for('serve_student_image', student_id=student.id, image_type='artwork'))
        
        response_students.append(student_response)
        
    return response_students
