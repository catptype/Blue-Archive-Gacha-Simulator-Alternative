from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from typing import Optional

from . import models, schemas
from .database import engine, get_db

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS Middleware ---
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- API Endpoints ---

@app.get("/api/schools/", response_model=list[schemas.SchoolResponse])
def get_schools(request: Request, db: Session = Depends(get_db)):
    db_schools = db.query(models.School).all()
    
    response_schools = []
    for school in db_schools:
        # Use model_validate instead of from_orm
        school_data = schemas.SchoolResponse.model_validate(school)
        school_data.school_id = school.school_id
        if school.school_image:
            school_data.image_url = str(request.url_for('serve_school_image', school_id=school.school_id))
        response_schools.append(school_data)
        
    return response_schools

@app.get("/api/students/", response_model=list[schemas.StudentResponse])
def get_students(request: Request, school_id: Optional[int] = None, db: Session = Depends(get_db)):
    
    # Start with a base query
    students_query = (
        db.query(models.Student)
        .options(joinedload(models.Student.school), joinedload(models.Student.version), joinedload(models.Student.asset))
    )
    
    # If a school_id was provided in the URL, apply the filter
    if school_id is not None:
        students_query = students_query.filter(models.Student.school_id_fk == school_id)

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

# --- Image Serving Endpoints (No changes needed here) ---

@app.get("/image/school/{school_id}", name="serve_school_image")
def serve_school_image(school_id: int, db: Session = Depends(get_db)):
    school = db.query(models.School).filter(models.School.school_id == school_id).first()
    if not school or not school.school_image:
        raise HTTPException(status_code=404, detail="School image not found")
    return Response(content=school.school_image, media_type="image/png")

@app.get("/image/student/{student_id}/{image_type}", name="serve_student_image")
def serve_student_image(student_id: int, image_type: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).options(joinedload(models.Student.asset)).filter(models.Student.student_id == student_id).first()
    
    if not student or not student.asset:
        raise HTTPException(status_code=404, detail="Student asset not found")

    image_data = None
    if image_type == "portrait":
        image_data = student.asset.asset_portrait_data
    elif image_type == "artwork":
        image_data = student.asset.asset_artwork_data
    
    if not image_data:
        raise HTTPException(status_code=404, detail="Image data not found for this type")
        
    return Response(content=image_data, media_type="image/png")