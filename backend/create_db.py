import json
import base64
import hashlib
from decimal import Decimal
from pathlib import Path
from typing import List, Dict, Any

# Important: This script assumes it is run from the `backend` directory.
# It uses relative paths to find the database and data files.
from backend.database import SessionLocal, engine
from .database import Base, SessionLocal
from .models import (
    Version, School, ImageAsset, Student, GachaPreset, GachaBanner
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


def seed_versions(db):
    """
    Seeds the Version table, guaranteeing that "Original" has version_id=1.
    """
    print("Seeding Versions...")

    # --- Phase 1: Handle the "Original" version special case ---
    # Check if the "Original" version already exists.
    original_in_db = db.query(Version).filter_by(version_name="Original").first()
    
    # If it doesn't exist, add it. Since this is the first operation on a
    # clean table, it will be assigned ID 1 by the database.
    if not original_in_db:
        print("  - Adding special case: Original (ensuring ID 1)")
        original_version = Version(version_name="Original")
        db.add(original_version)
        # We commit here to finalize this transaction before proceeding.
        db.commit()
    
    # --- Phase 2: Handle all other versions found in data files ---
    # 1. Load all student data to find all unique versions.
    all_student_data = load_json_files_from_dir(DATA_DIR / "students")
    unique_versions = {student_data['version'] for student_data in all_student_data}
    
    # 2. Get a list of other versions, explicitly excluding "Original".
    other_versions = sorted([v for v in unique_versions if v != "Original"])

    # 3. Add the remaining versions if they don't already exist.
    for name in other_versions:
        exists = db.query(Version).filter_by(version_name=name).first()
        if not exists:
            new_version = Version(version_name=name)
            db.add(new_version)
            print(f"  - Added Version: {name}")

    # Commit the rest of the new versions.
    db.commit()


def seed_schools(db):
    """Seeds the School table from schools.json."""
    print("\nSeeding Schools...")
    with open(DATA_DIR / "schools.json", "r") as f:
        schools_data = json.load(f)
    
    for school_data in schools_data:
        name = school_data['name']
        exists = db.query(School).filter_by(school_name=name).first()
        if not exists:
            image_bytes = base64.b64decode(school_data['image_base64'])
            new_school = School(school_name=name, school_image=image_bytes)
            db.add(new_school)
            print(f"  - Added School: {name}")
    db.commit()


def seed_students(db):
    """Seeds ImageAsset and Student tables from the students/ directory."""
    print("\nSeeding Students...")
    student_files = (DATA_DIR / "students").glob("*.json")
    
    for file_path in student_files:
        with open(file_path, "r") as f:
            student_data = json.load(f)

        # Find related version and school, which must already exist
        version_obj = db.query(Version).filter_by(version_name=student_data['version']).one_or_none()
        school_obj = db.query(School).filter_by(school_name=student_data['school']).one_or_none()

        if not version_obj or not school_obj:
            print(f"  - SKIPPING {student_data['name']} ({student_data['version']}): Missing required Version or School.")
            continue

        # Check if this specific student already exists
        exists = db.query(Student).filter_by(
            student_name=student_data['name'], 
            version_id_fk=version_obj.version_id
        ).first()

        if not exists:
            # 1. Create the ImageAsset first
            portrait_bytes = base64.b64decode(student_data['base64']['portrait'])
            artwork_bytes = base64.b64decode(student_data['base64']['artwork'])
            
            # Replicate Django's hashing logic
            p_hash = hashlib.sha256(portrait_bytes).hexdigest()
            f_hash = hashlib.sha256(artwork_bytes).hexdigest()
            combined_hash = hashlib.sha256(f"{p_hash}-{f_hash}".encode()).hexdigest()

            new_asset = ImageAsset(
                asset_portrait_data=portrait_bytes,
                asset_artwork_data=artwork_bytes,
                asset_pair_hash=combined_hash
            )
            db.add(new_asset)
            db.flush() # Flush to assign an ID to new_asset

            # 2. Create the Student
            new_student = Student(
                student_name=student_data['name'],
                student_rarity=student_data['rarity'],
                student_is_limited=student_data['is_limited'],
                version_id_fk=version_obj.version_id,
                school_id_fk=school_obj.school_id,
                asset_id_fk=new_asset.asset_id
            )
            db.add(new_student)
            print(f"  - Added Student: {student_data['name']} ({student_data['version']})")
    db.commit()


def seed_presets(db):
    """Seeds GachaPreset table from presets.json."""
    print("\nSeeding Gacha Presets...")
    with open(DATA_DIR / "presets.json", "r") as f:
        presets_data = json.load(f)
    
    for preset_data in presets_data:
        name = preset_data['name']
        exists = db.query(GachaPreset).filter_by(preset_name=name).first()
        if not exists:
            new_preset = GachaPreset(
                preset_name=name,
                preset_pickup_rate=Decimal(preset_data['pickup']),
                preset_r3_rate=Decimal(preset_data['r3']),
                preset_r2_rate=Decimal(preset_data['r2']),
                preset_r1_rate=Decimal(preset_data['r1'])
            )
            db.add(new_preset)
            print(f"  - Added Preset: {name}")
    db.commit()


def seed_banners(db):
    """Seeds GachaBanner table from the banners/ directory."""
    print("\nSeeding Banners...")
    banner_files = (DATA_DIR / "banners").glob("*.json")
    
    for file_path in banner_files:
        with open(file_path, "r") as f:
            banner_data = json.load(f)
        
        name = banner_data['name']
        exists = db.query(GachaBanner).filter_by(banner_name=name).first()

        if not exists:
            # Find related preset
            preset_obj = db.query(GachaPreset).filter_by(preset_name=banner_data['preset']).one()
            
            # Find related versions for the pool
            versions_in_pool = db.query(Version).filter(Version.version_name.in_(banner_data['version'])).all()
            
            # Find related students for pickup
            pickup_students = []
            for pickup_info in banner_data['pickup']:
                version = db.query(Version).filter_by(version_name=pickup_info['version']).one()
                student = db.query(Student).filter_by(student_name=pickup_info['name'], version_id_fk=version.version_id).one()
                pickup_students.append(student)

            image_bytes = base64.b64decode(banner_data['image_base64'])

            new_banner = GachaBanner(
                banner_name=name,
                banner_image=image_bytes,
                banner_include_limited=banner_data['limited'],
                preset_id_fk=preset_obj.preset_id,
                included_versions=versions_in_pool,
                pickup_students=pickup_students
            )
            db.add(new_banner)
            print(f"  - Added Banner: {name}")
    db.commit()


def main():
    """Main function to run all seeding operations."""

    # Create database tables
    print("Initializing database and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

    # Use a session that is automatically closed
    with SessionLocal() as db:
        seed_versions(db)
        seed_schools(db)
        seed_students(db)
        seed_presets(db)
        seed_banners(db)
    print("\nDatabase seeding complete!")


if __name__ == "__main__":
    main()