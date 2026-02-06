import base64
import hashlib
import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload

from typing import Callable, Tuple

from ..util.cache import get_cache, Cache
from ..util.database import get_db

from ..config import settings
from ..util.models import Achievement, Student, School, GachaBanner

LOGGER = logging.getLogger(__name__)

router = APIRouter()

# --- Helper functions

def serve_image(
    request: Request,
    cache: Cache,
    cache_key: str,
    fetch_data_func: Callable[[], Tuple[bytes, str]], # Returns (bytes, filename)
):

    # Default variables
    etag = None
    filename = "image.png"
    
    # Get meta data from cache
    cached_data = cache.get(cache_key)
    if cached_data:
        etag = cached_data['etag']
        
        # Check Browser Cache
        if request.headers.get("if-none-match") == etag:
            LOGGER.debug(f"CACHE HIT (Browser - 304) for {cache_key}")
            return Response(status_code=304)
        
    # Get image data from db
    LOGGER.debug(f"FETCHING DATA for {cache_key}")
    image_bytes, filename = fetch_data_func()
    
    if not image_bytes:
        raise HTTPException(status_code=404, detail="Image data not found")

    # Generate ETag
    etag = hashlib.sha1(image_bytes).hexdigest()

    # Save to Cache
    data_to_cache = {
        "etag": etag,
        "filename": filename
    }
    cache.set(cache_key, data_to_cache, expire=settings.CACHE_EXPIRE)

    # Check Browser Cache (DB Path)
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)

    # Send response
    headers = {
        "Cache-Control": "public, max-age=86400",
        "ETag": etag,
        "Content-Disposition": f'inline; filename="{filename}"'
    }
    return Response(content=image_bytes, media_type="image/png", headers=headers)

# --- Endpoints ---

@router.get("/achievement/{achievement_id}", tags=["images"], name="serve_achievement_image")
def serve_achievement_image(achievement_id: int, request: Request, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):
    cache_key = f"image:achievement:{achievement_id}"
    
    def fetch_achievement():
        obj = db.query(Achievement).filter_by(id=achievement_id).first()
        if not obj or not obj.image_data:
            raise HTTPException(status_code=404, detail="Not found")
        
        return obj.image_data, f"{obj.key}.png"
    
    return serve_image(request, cache, cache_key, fetch_achievement)

@router.get("/banner/{banner_id}", tags=["images"], name="serve_banner_image")
def serve_banner_image(banner_id: int, request: Request, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):
    cache_key = f"image:banner:{banner_id}"
    
    def fetch_banner():
        obj = db.query(GachaBanner).filter_by(id=banner_id).first()
        if not obj or not obj.image_data:
            raise HTTPException(status_code=404, detail="Not found")
        
        return obj.image_data, f"{obj.name}.png"
    
    return serve_image(request, cache, cache_key, fetch_banner)

@router.get("/school/{school_id}", tags=["images"], name="serve_school_image")
def serve_school_image(school_id: int, request: Request, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):
    
    cache_key = f"image:school:{school_id}"
    def fetch_school():
        obj = db.query(School).filter_by(id=school_id).first()
        if not obj or not obj.image_data:
            raise HTTPException(status_code=404, detail="Not found")
        
        return obj.image_data, f"{obj.name}.png"
    
    return serve_image(request, cache, cache_key, fetch_school)

@router.get("/student/{student_id}/{image_type}", tags=["images"], name="serve_student_image")
def serve_student_image(student_id: int, image_type: str, request: Request, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):
    
    if image_type not in ["portrait", "artwork"]:
        raise HTTPException(status_code=400, detail="Invalid image type")

    cache_key = f"image:student:{student_id}:{image_type}"

    def fetch_student():
        obj = db.query(Student).options(
            joinedload(Student.asset),
            joinedload(Student.version) # Load version for the filename
        ).filter(Student.id == student_id).first()

        if not obj or not obj.asset:
            raise HTTPException(status_code=404, detail="Student asset not found")
        
        # Logic to pick the column
        img_data = None
        if image_type == "portrait":
            img_data = obj.asset.portrait_data
        elif image_type == "artwork":
            img_data = obj.asset.artwork_data
        
        if not img_data:
             raise HTTPException(status_code=404, detail=f"No data for {image_type}")
        
        filename = f"{obj.name}_{obj.version.name}_{image_type}.png"
        return img_data, filename
    
    return serve_image(request, cache, cache_key, fetch_student)
