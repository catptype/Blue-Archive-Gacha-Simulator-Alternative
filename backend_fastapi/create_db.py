import json
import base64
import hashlib
from decimal import Decimal
from pathlib import Path
from typing import List, Dict, Any
from sqlalchemy.orm.session import Session

# Important: This script assumes it is run from the `backend` directory.
# It uses relative paths to find the database and data files.
# from backend.util.database import SessionLocal, engine
from .util.database import Base, SessionLocal, engine
from .util.models import (
    Version, School, ImageAsset, Student, GachaPreset, GachaBanner, User, Role, Achievement
)

# Define the path to your data directory
DATA_DIR = Path(__file__).parent / "data"

def load_json_files_from_dir(directory: Path) -> List[Dict[str, Any]]:
    """Loads all JSON files from a specified directory."""
    data_list = []
    for file_path in directory.glob("*.json"):
        with open(file_path, "r") as f:
            data_list.append(json.load(f))
    return data_list

def seed_roles(db: Session):
    """Seeds the Role table with predefined roles."""
    print("Seeding Roles...")
    
    # Define your application's roles here
    role_list = ["superuser", "member"]
    for name in role_list:
        exists = db.query(Role).filter_by(name=name).first()
        if not exists:
            new_role = Role(name=name)
            db.add(new_role)
            print(f"  - Added Role: {name}")
    db.commit()

def seed_versions(db: Session):
    """
    Seeds the Version table, guaranteeing that "Original" has version_id=1.
    """
    print("Seeding Versions...")

    # --- Phase 1: Handle the "Original" version special case ---
    original_is_exist = db.query(Version.id).filter_by(name="Original").first()
    if not original_is_exist:
        print("  - Adding special case: Original (ensuring ID 1)")
        original_version = Version(name="Original")
        db.add(original_version)
        db.commit()
    
    # --- Phase 2: Handle all other versions found in data files ---
    # Load all student data to find all unique versions.
    all_student_data = load_json_files_from_dir(DATA_DIR / "students")
    all_versions = {student_data['version'] for student_data in all_student_data}
    non_orig_versions = sorted([v for v in all_versions if v != "Original"])

    # Add the remaining versions if they don't already exist.
    for name in non_orig_versions:
        exists = db.query(Version).filter_by(name=name).first()
        if not exists:
            new_version = Version(name=name)
            db.add(new_version)
            print(f"  - Added Version: {name}")

    db.commit()

def seed_schools(db: Session):
    """Seeds the School table from schools.json."""
    print("\nSeeding Schools...")
    with open(DATA_DIR / "schools.json", "r") as f:
        school_json_list = json.load(f)
    
    for school_json in school_json_list:
        name = school_json['name']
        image_b64 = school_json['image_base64']
        exists = db.query(School).filter_by(name=name).first()
        if not exists:
            image_bytes = base64.b64decode(image_b64)
            new_school = School(name=name, image_data=image_bytes)
            db.add(new_school)
            print(f"  - Added School: {name}")
    db.commit()

def seed_students(db: Session):
    """Seeds ImageAsset and Student tables from the students/ directory."""
    print("\nSeeding Students...")
    student_files = (DATA_DIR / "students").glob("*.json")
    cache = {}
    for file_path in student_files:
        with open(file_path, "r") as f:
            student_data = json.load(f)

        student_name = student_data['name']
        student_version = student_data['version']
        student_school = student_data['school']
        student_rarity = student_data['rarity']
        student_is_limited = student_data['is_limited']
        student_portrait_data = student_data['base64']['portrait']
        student_artwork_data = student_data['base64']['artwork']

        # Find related version and school, which must already exist
        version_key = f"version:{student_version}"
        version_obj = cache.get(version_key, None)
        if version_obj is None:
            version_obj = db.query(Version).filter_by(name=student_version).first()
            if not version_obj :
                print(f"  - SKIPPING {student_name} ({student_version}): Missing required Version.")
                continue
            cache[version_key] = version_obj
        
        school_key = f"school:{student_school}"
        school_obj = cache.get(school_key, None)
        if school_obj is None:
            school_obj = db.query(School).filter_by(name=student_school).first()
            if not school_obj:
                print(f"  - SKIPPING {student_name} ({student_version}): Missing required School.")
                continue
            cache[school_key] = school_obj

        # Check if this specific student already exists
        exists = db.query(Student).filter_by(
            name=student_name, 
            version_id=version_obj.id
        ).first()

        if not exists:
            # 1. Create the ImageAsset first
            portrait_bytes = base64.b64decode(student_portrait_data)
            artwork_bytes = base64.b64decode(student_artwork_data)
            
            # Replicate hashing logic
            p_hash = hashlib.sha256(portrait_bytes).hexdigest()
            f_hash = hashlib.sha256(artwork_bytes).hexdigest()
            combined_hash = hashlib.sha256(f"{p_hash}-{f_hash}".encode()).hexdigest()

            new_asset = ImageAsset(
                portrait_data=portrait_bytes,
                artwork_data=artwork_bytes,
                pair_hash=combined_hash
            )
            db.add(new_asset)
            db.flush() # Flush to assign an ID to new_asset

            # 2. Create the Student
            new_student = Student(
                name=student_name,
                rarity=student_rarity,
                is_limited=student_is_limited,
                version_id=version_obj.id,
                school_id=school_obj.id,
                asset_id=new_asset.id
            )
            db.add(new_student)
            print(f"  - Added Student: {student_name} ({student_version})")
    db.commit()

def seed_presets(db: Session):
    """Seeds GachaPreset table from presets.json."""
    print("\nSeeding Gacha Presets...")
    with open(DATA_DIR / "presets.json", "r") as f:
        presets_data = json.load(f)
    
    for preset_data in presets_data:
        name = preset_data['name']
        is_exists = db.query(GachaPreset.id).filter_by(name=name).first()
        if not is_exists:
            new_preset = GachaPreset(
                name=name,
                pickup_rate=Decimal(preset_data['pickup']),
                r3_rate=Decimal(preset_data['r3']),
                r2_rate=Decimal(preset_data['r2']),
                r1_rate=Decimal(preset_data['r1'])
            )
            db.add(new_preset)
            print(f"  - Added Preset: {name}")
    db.commit()

def seed_banners(db: Session):
    """Seeds GachaBanner table from the banners/ directory."""
    print("\nSeeding Banners...")
    banner_files = (DATA_DIR / "banners").glob("*.json")
    
    for file_path in banner_files:
        with open(file_path, "r") as f:
            banner_data = json.load(f)
        
        banner_name = banner_data['name']
        banner_preset = banner_data['preset']
        banner_version_list = banner_data['version']
        banner_pickup_list = banner_data['pickup']
        banner_limited = banner_data['limited']
        banner_image_data = banner_data['image_base64']

        exists = db.query(GachaBanner.id).filter_by(name=banner_name).first()

        if not exists:
            # Find related preset
            preset_obj = db.query(GachaPreset).filter_by(name=banner_preset).one()
            
            # Find related versions for the pool
            version_obj_list = db.query(Version).filter(Version.name.in_(banner_version_list)).all()
            
            # Find related students for pickup
            pickup_students = []
            for student_data in banner_pickup_list:
                student_obj = db.query(Student).join(Version).filter(
                    Student.name == student_data['name'],
                    Version.name == student_data['version']
                ).one()
                pickup_students.append(student_obj)

            image_bytes = base64.b64decode(banner_image_data)

            new_banner = GachaBanner(
                name=banner_name,
                image_data=image_bytes,
                include_limited=banner_limited,
                included_versions=version_obj_list,
                preset_id=preset_obj.id,
                pickup_students=pickup_students
            )
            db.add(new_banner)
            print(f"  - Added Banner: {banner_name}")
    db.commit()

def seed_achievements(db: Session):
    """Seeds the Achievement table from the achievements/ directory."""
    print("\nSeeding Achievements...")
    all_achievement_data = load_json_files_from_dir(DATA_DIR / "achievements")
    
    for ach_data in all_achievement_data:
        key = ach_data.get('key')
        if not key:
            print("  - SKIPPING achievement file with no 'key'.")
            continue

        # Check if an achievement with this unique key already exists
        exists = db.query(Achievement.id).filter_by(key=key).first()
        if not exists:

            category = ach_data.get('category', 'MILESTONE')
            name = ach_data.get('name', 'Unnamed Achievement')
            description = ach_data.get('description')
            # Decode the image if it exists
            image_b64 = ach_data.get('image_base64')
            image_bytes = base64.b64decode(image_b64) if image_b64 else None

            # Create the new Achievement instance
            new_achievement = Achievement(
                key=key,
                category=category,
                name=name,
                description=description,
                image_data=image_bytes
            )
            db.add(new_achievement)
            print(f"  - Added Achievement: {name}")
            
    db.commit()

def main():
    """Main function to run all seeding operations."""

    # Create database tables
    print("Initializing database and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

    # Use a session that is automatically closed
    with SessionLocal() as db:
        seed_roles(db)
        seed_versions(db)
        seed_schools(db)
        seed_students(db)
        seed_presets(db)
        seed_banners(db)
        seed_achievements(db)
    print("\nDatabase seeding complete!")

if __name__ == "__main__":
    main()