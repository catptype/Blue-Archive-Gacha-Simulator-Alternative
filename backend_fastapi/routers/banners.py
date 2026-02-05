import logging
from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List

from ..util.models import GachaBanner, Student
from ..util.cache import get_cache, Cache
from ..util.database import get_db
from ..util.schemas.BannerResponse import BannerResponse, BannerDetailResponse
from ..util.schemas.StudentResponse import StudentResponse, create_student_response
from ..config import settings

LOGGER = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", tags=["banners"], response_model=List[BannerResponse])
def get_banners(request: Request, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):
    cache_key = "all_banners"

    # Get all banner data from cache
    cached_data = cache.get(cache_key)
    if cached_data:
        # Convert from dict to pydatic schema
        LOGGER.debug(f"CACHE HIT ({cache_key})")
        return [BannerResponse.model_validate(item) for item in cached_data]

    # Get all banner data from db
    LOGGER.debug(f"CACHE MISS ({cache_key})")
    banner_list = db.query(GachaBanner).all()

    # Prepare response data following pydatic schema
    response_banners:List[BannerResponse] = []
    for banner in banner_list:
        banner_data = BannerResponse.model_validate(banner)
        if banner.image_data:
            banner_data.image_url = str(request.url_for('serve_banner_image', banner_id=banner.id))
        response_banners.append(banner_data)

    # Convert format to dict for saving cache
    banners_to_cache = [b.model_dump(model='json') for b in response_banners]
    cache.set(cache_key, banners_to_cache, expire=settings.CACHE_EXPIRE)
        
    return response_banners

@router.get("/{banner_id}/details/", tags=["banners"], response_model=BannerDetailResponse)
def get_banner_details(banner_id: int, request: Request, db: Session = Depends(get_db)):

    # Check banner is exist    
    db_banner = db.query(GachaBanner).options(
        selectinload(GachaBanner.pickup_students),
        selectinload(GachaBanner.included_versions),
        selectinload(GachaBanner.excluded_students)
    ).filter_by(id=banner_id).first() 

    if not db_banner:
        raise HTTPException(status_code=404, detail="Banner not found")

    # Get pickup and excluded student IDs
    pickup_ids = {s.id for s in db_banner.pickup_students}
    excluded_ids = {s.id for s in db_banner.excluded_students}
    
    # Get version IDs
    included_version_ids = {v.id for v in db_banner.included_versions}

    # Query only students available in banner from all students
    all_students_obj = db.query(Student).options(
        joinedload(Student.school), 
        joinedload(Student.version), 
        joinedload(Student.asset)
    ).filter(
        Student.version_id.in_(included_version_ids),
        Student.id.not_in(excluded_ids),
        Student.is_limited == db_banner.include_limited
    ).all()
    
    # Prepare response following schema
    base_banner_response = BannerResponse.model_validate(db_banner)
    if db_banner.image_data:
        base_banner_response.image_url = str(request.url_for('serve_banner_image', banner_id=db_banner.id)) 

    # StudentResponse
    pickup_r3_list: List[StudentResponse] = []
    nonpickup_r3_list: List[StudentResponse] = []
    r2_list: List[StudentResponse] = []
    r1_list: List[StudentResponse] = []

    for student_obj in all_students_obj:
        response = create_student_response(student_obj, request)
        
        if student_obj.rarity == 3:
            if student_obj.id in pickup_ids:
                pickup_r3_list.append(response)
            else:
                nonpickup_r3_list.append(response)
        elif student_obj.rarity == 2:
            r2_list.append(response)
        elif student_obj.rarity == 1:
            r1_list.append(response)

    # Combine all
    final_response = BannerDetailResponse(
        **base_banner_response.model_dump(),
        pickup_r3_students=pickup_r3_list,
        nonpickup_r3_students=nonpickup_r3_list,
        r2_students=r2_list,
        r1_students=r1_list
    )

    return final_response