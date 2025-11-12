import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, LargeBinary, Numeric, DateTime, Table, UniqueConstraint, Text
)
from sqlalchemy.orm import relationship
from .database import Base

# ==============================================================================
# ASSOCIATION TABLES FOR MANY-TO-MANY RELATIONSHIPS
# ==============================================================================

# Association table for GachaBanner <-> Version
banner_version_association = Table('banner_version_association', Base.metadata,
    Column('banner_id', Integer, ForeignKey('gacha_banner_table.banner_id')),
    Column('version_id', Integer, ForeignKey('student_version_table.version_id'))
)

# Association table for GachaBanner <-> Student (for Pickups)
banner_pickup_association = Table('banner_pickup_association', Base.metadata,
    Column('banner_id', Integer, ForeignKey('gacha_banner_table.banner_id')),
    Column('student_id', Integer, ForeignKey('student_table.student_id'))
)

# Association table for GachaBanner <-> Student (for Exclusions)
banner_exclude_association = Table('banner_exclude_association', Base.metadata,
    Column('banner_id', Integer, ForeignKey('gacha_banner_table.banner_id')),
    Column('student_id', Integer, ForeignKey('student_table.student_id'))
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
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, nullable=False)

    def __str__(self) -> str:
        return self.role_name

class User(Base):
    __tablename__ = 'user_table'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id_fk = Column(Integer, ForeignKey('role_table.role_id'), nullable=False)
    role = relationship("Role")

    def __str__(self) -> str:
        return self.username


# ==============================================================================
# MAIN DATA MODELS
# ==============================================================================

class Version(Base):
    __tablename__ = 'student_version_table'
    version_id = Column(Integer, primary_key=True, index=True)
    version_name = Column(String, unique=True, nullable=False)

    def __str__(self) -> str:
        return self.version_name

class School(Base):
    __tablename__ = 'student_school_table'
    school_id = Column(Integer, primary_key=True, index=True)
    school_name = Column(String, unique=True, nullable=False)
    school_image = Column(LargeBinary, nullable=True)

    def __str__(self) -> str:
        return self.school_name

class ImageAsset(Base):
    __tablename__ = 'image_asset_table'
    asset_id = Column(Integer, primary_key=True, index=True)
    asset_portrait_data = Column(LargeBinary, nullable=True)
    asset_artwork_data = Column(LargeBinary, nullable=True)
    asset_pair_hash = Column(String(64), unique=True, nullable=False)

class Student(Base):
    __tablename__ = 'student_table'
    student_id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    student_rarity = Column(Integer, nullable=False)
    student_is_limited = Column(Boolean, default=False)
    version_id_fk = Column(Integer, ForeignKey('student_version_table.version_id'))
    school_id_fk = Column(Integer, ForeignKey('student_school_table.school_id'))
    asset_id_fk = Column(Integer, ForeignKey('image_asset_table.asset_id'), nullable=True)

    version = relationship("Version", lazy='selectin')
    school = relationship("School", lazy='selectin')
    asset = relationship("ImageAsset", uselist=False, lazy='joined')
    
    __table_args__ = (UniqueConstraint('student_name', 'version_id_fk', name='_student_version_uc'),)

    def __str__(self) -> str:
        return f"{self.student_name} ({self.version})"


class GachaPreset(Base):
    __tablename__ = 'gacha_preset_table'
    preset_id = Column(Integer, primary_key=True, index=True)
    preset_name = Column(String, unique=True, nullable=False)
    preset_pickup_rate = Column(Numeric(4, 1), nullable=False)
    preset_r3_rate = Column(Numeric(4, 1), nullable=False)
    preset_r2_rate = Column(Numeric(4, 1), nullable=False)
    preset_r1_rate = Column(Numeric(4, 1), nullable=False)

    def __str__(self) -> str:
        return f"{self.preset_name} ( {self.preset_pickup_rate} | ★★★ {self.preset_r3_rate} | ★★ {self.preset_r2_rate} | ★ {self.preset_r1_rate} )"

class GachaBanner(Base):
    __tablename__ = 'gacha_banner_table'
    banner_id = Column(Integer, primary_key=True, index=True)
    banner_image = Column(LargeBinary, nullable=True)
    banner_name = Column(String, unique=True, nullable=False)
    banner_include_limited = Column(Boolean, default=False)
    preset_id_fk = Column(Integer, ForeignKey('gacha_preset_table.preset_id'), nullable=True)
    
    preset = relationship("GachaPreset", lazy='joined')
    
    # Many-to-Many relationships defined using the association tables
    included_versions = relationship("Version", secondary=banner_version_association, lazy='selectin')
    pickup_students = relationship("Student", secondary=banner_pickup_association, lazy='selectin')
    excluded_students = relationship("Student", secondary=banner_exclude_association, lazy='selectin')

class GachaTransaction(Base):
    __tablename__ = 'gacha_transaction_table'
    transaction_id = Column(Integer, primary_key=True, index=True)
    transaction_create_on = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    user_id_fk = Column(Integer, ForeignKey('user_table.user_id'))
    banner_id_fk = Column(Integer, ForeignKey('gacha_banner_table.banner_id'))
    student_id_fk = Column(Integer, ForeignKey('student_table.student_id'))

    user = relationship("User", lazy='selectin')
    banner = relationship("GachaBanner", lazy='selectin')
    student = relationship("Student", lazy='selectin')

class UserInventory(Base):
    __tablename__ = 'user_inventory_table'
    inventory_id = Column(Integer, primary_key=True, index=True)
    inventory_num_obtained = Column(Integer, default=1)
    inventory_first_obtained_on = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    user_id_fk = Column(Integer, ForeignKey('user_table.user_id'))
    student_id_fk = Column(Integer, ForeignKey('student_table.student_id'))

    user = relationship("User", lazy='selectin')
    student = relationship("Student", lazy='selectin')
    
    __table_args__ = (UniqueConstraint('user_id_fk', 'student_id_fk', name='_user_student_uc'),)

class Achievement(Base):
    __tablename__ = 'achievement_table'
    achievement_id = Column(Integer, primary_key=True, index=True)
    achievement_name = Column(String, unique=True, nullable=False)
    achievement_description = Column(Text, nullable=True)
    achievement_image = Column(LargeBinary, nullable=True)
    achievement_category = Column(String(20), default='MILESTONE')
    achievement_key = Column(String(50), unique=True, nullable=False)

    def __str__(self) -> str:
        return f"{self.achievement_name}"

class UnlockAchievement(Base):
    __tablename__ = 'unlock_achievement_table'
    unlock_id = Column(Integer, primary_key=True, index=True)
    unlock_on = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    user_id_fk = Column(Integer, ForeignKey('user_table.user_id'))
    achievement_id_fk = Column(Integer, ForeignKey('achievement_table.achievement_id'))

    user = relationship("User", lazy='selectin')
    achievement = relationship("Achievement", lazy='selectin')

    __table_args__ = (UniqueConstraint('user_id_fk', 'achievement_id_fk', name='_user_achievement_uc'),)