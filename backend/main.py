from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload
from typing import Optional

from . import models, schemas, auth
from .database import engine, get_db
from datetime import timedelta
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS Middleware ---
origins = ["http://localhost:5173", "http://localhost:5173"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

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