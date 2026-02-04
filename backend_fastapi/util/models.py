import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, LargeBinary, Numeric, DateTime, Table, UniqueConstraint, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGBLOB
from .database import Base

BLOB_TYPE = LargeBinary().with_variant(LONGBLOB, "mysql", "mariadb")
DEFAULT_UTC_NOW = lambda: datetime.datetime.now(datetime.timezone.utc)

# ==============================================================================
# ASSOCIATION TABLES FOR MANY-TO-MANY RELATIONSHIPS
# ==============================================================================

# Association table for GachaBanner <-> Version
banner_version_association = Table('banner_version_association', Base.metadata,
    Column('banner_id', Integer, ForeignKey('gacha_banner_table.id')),
    Column('version_id', Integer, ForeignKey('student_version_table.id'))
)

# Association table for GachaBanner <-> Student (for Pickups)
banner_pickup_association = Table('banner_pickup_association', Base.metadata,
    Column('banner_id', Integer, ForeignKey('gacha_banner_table.id')),
    Column('student_id', Integer, ForeignKey('student_table.id'))
)

# Association table for GachaBanner <-> Student (for Exclusions)
banner_exclude_association = Table('banner_exclude_association', Base.metadata,
    Column('banner_id', Integer, ForeignKey('gacha_banner_table.id')),
    Column('student_id', Integer, ForeignKey('student_table.id'))
)

# ==============================================================================
# A PLACEHOLDER USER MODEL
# ==============================================================================
# FastAPI doesn't have a built-in User model like Django.
# You would typically implement authentication separately (e.g., with OAuth2/JWT).
# This model serves as a placeholder for the foreign key relationships.

# --- ADD THIS NEW MODEL ---
class Role(Base):
    __tablename__ = 'role_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)

    def __str__(self) -> str:
        return self.name

class User(Base):
    __tablename__ = 'user_table'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('role_table.id'), nullable=False)
    role = relationship("Role")

    def __str__(self) -> str:
        return self.username

# ==============================================================================
# MAIN DATA MODELS
# ==============================================================================

class Version(Base):
    __tablename__ = 'student_version_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)

    def __str__(self) -> str:
        return self.name

class School(Base):
    __tablename__ = 'student_school_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)
    image_data = Column(BLOB_TYPE, nullable=True)

    def __str__(self) -> str:
        return self.name

class ImageAsset(Base):
    __tablename__ = 'image_asset_table'
    id = Column(Integer, primary_key=True, index=True)
    portrait_data = Column(BLOB_TYPE, nullable=True)
    artwork_data = Column(BLOB_TYPE, nullable=True)
    pair_hash = Column(String(64), unique=True, nullable=False)

class Student(Base):
    __tablename__ = 'student_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    rarity = Column(Integer, nullable=False)
    is_limited = Column(Boolean, default=False)
    version_id = Column(Integer, ForeignKey('student_version_table.id'))
    school_id = Column(Integer, ForeignKey('student_school_table.id'))
    asset_id = Column(Integer, ForeignKey('image_asset_table.id'), nullable=True)

    version = relationship("Version", lazy='selectin')
    school = relationship("School", lazy='selectin')
    asset = relationship("ImageAsset", uselist=False, lazy='joined')
    
    __table_args__ = (UniqueConstraint('name', 'version_id', name='_student_version_uc'),)

    def __str__(self) -> str:
        return f"{self.name} ({self.version})"

class GachaPreset(Base):
    __tablename__ = 'gacha_preset_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)
    pickup_rate = Column(Numeric(4, 1), nullable=False)
    r3_rate = Column(Numeric(4, 1), nullable=False)
    r2_rate = Column(Numeric(4, 1), nullable=False)
    r1_rate = Column(Numeric(4, 1), nullable=False)

    def __str__(self) -> str:
        return f"{self.name} ( {self.pickup_rate} | ★★★ {self.r3_rate} | ★★ {self.r2_rate} | ★ {self.r1_rate} )"

class GachaBanner(Base):
    __tablename__ = 'gacha_banner_table'
    id = Column(Integer, primary_key=True, index=True)
    image_data = Column(BLOB_TYPE, nullable=True)
    name = Column(String(20), unique=True, nullable=False)
    include_limited = Column(Boolean, default=False)
    preset_id = Column(Integer, ForeignKey('gacha_preset_table.id'), nullable=True)
    preset = relationship("GachaPreset", lazy='joined')
    
    # Many-to-Many relationships defined using the association tables
    included_versions = relationship("Version", secondary=banner_version_association, lazy='selectin')
    pickup_students = relationship("Student", secondary=banner_pickup_association, lazy='selectin')
    excluded_students = relationship("Student", secondary=banner_exclude_association, lazy='selectin')

class GachaTransaction(Base):
    __tablename__ = 'gacha_transaction_table'
    id = Column(Integer, primary_key=True, index=True)
    create_on = Column(DateTime, default=DEFAULT_UTC_NOW)
    
    user_id = Column(Integer, ForeignKey('user_table.id'))
    banner_id = Column(Integer, ForeignKey('gacha_banner_table.id'))
    student_id = Column(Integer, ForeignKey('student_table.id'))

    user = relationship("User", lazy='selectin')
    banner = relationship("GachaBanner", lazy='selectin')
    student = relationship("Student", lazy='selectin')

class UserInventory(Base):
    __tablename__ = 'user_inventory_table'
    id = Column(Integer, primary_key=True, index=True)
    num_obtained = Column(Integer, default=1)
    first_obtained_on = Column(DateTime, default=DEFAULT_UTC_NOW)
    
    user_id = Column(Integer, ForeignKey('user_table.id'))
    student_id = Column(Integer, ForeignKey('student_table.id'))

    user = relationship("User", lazy='selectin')
    student = relationship("Student", lazy='selectin')
    
    __table_args__ = (UniqueConstraint('user_id', 'student_id', name='_user_student_uc'),)

class Achievement(Base):
    __tablename__ = 'achievement_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    image_data = Column(BLOB_TYPE, nullable=True)
    category = Column(String(20), default='MILESTONE')
    key = Column(String(50), unique=True, nullable=False)

    def __str__(self) -> str:
        return f"{self.name}"

class UnlockAchievement(Base):
    __tablename__ = 'unlock_achievement_table'
    id = Column(Integer, primary_key=True, index=True)
    unlock_on = Column(DateTime, default=DEFAULT_UTC_NOW)
    
    user_id = Column(Integer, ForeignKey('user_table.id'))
    achievement_id = Column(Integer, ForeignKey('achievement_table.id'))

    user = relationship("User", lazy='selectin')
    achievement = relationship("Achievement", lazy='selectin')

    __table_args__ = (UniqueConstraint('user_id', 'achievement_id', name='_user_achievement_uc'),)