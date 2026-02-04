from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from jose import jwt
from markupsafe import Markup

# Import your database engine and models
from .database import engine, SessionLocal
from .models import User, Role, Student, Version, School, GachaBanner, GachaPreset, GachaTransaction, Achievement, UnlockAchievement, UserInventory
from .auth import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_password
from .timezone import format_datetime_as_local
from datetime import timedelta

# --- 1. Define the Authentication Backend ---
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:

        form = await request.form()
        username, password = form["username"], form["password"]

        with SessionLocal() as db:
            user = db.query(User).filter_by(username=username).first()
            if user and verify_password(password, user.hashed_password) and user.role.name == "superuser":
                # Create a token for the session
                expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                token = create_access_token(data={"sub": user.username}, expires_delta=expires)
                request.session.update({"token": token})
                return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str | None = payload.get("sub")
            if not username:
                return False
            
            # Check if the user is a superuser
            with SessionLocal() as db:
                user = db.query(User).filter_by(username=username).first()
                if user:
                    return user.role.name == "superuser"
        except Exception:
            return False
            
        return False

# --- 2. Define the Model Views ---
# See icon at https://fontawesome.com/search?f=classic&s=solid&ic=free&o=r

class RoleAdmin(ModelView, model=Role):
    name = "Role"
    name_plural = "Roles"
    icon = "fa-solid fa-user-shield"
    column_list = [Role.id, Role.name]

class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-users"
    column_list = [User.id, User.username, User.role]
    column_details_exclude_list = [User.hashed_password]
    form_excluded_columns = [User.hashed_password]

class StudentAdmin(ModelView, model=Student):
    name = "Student"
    name_plural = "Students"
    icon = "fa-solid fa-graduation-cap"
    column_list = ["id", "Portrait", "name", "version", "rarity", "school"]
    column_searchable_list = [Student.name, "school.name", "version.name"]

    @staticmethod
    def _format_portrait(model: Student, _, size: int = 40) -> Markup:
        if model and model.asset:
            html_string = (
                f'<a href="/admin/student/details/{model.id}" title="{model}">'
                f'  <img src="/image/student/{model.id}/portrait" width="{size}" style="border-radius: 4px; margin: 2px;">'
                f'</a>'
            )
            return Markup(html_string)
        return ""
    
    @staticmethod
    def _format_artwork(model: Student, _, size: int = 40) -> Markup:
        if model and model.asset:
            html_string = (
                f'<a href="/admin/student/details/{model.id}" title="{model}">'
                f'  <img src="/image/student/{model.id}/artwork" width="{size}" style="border-radius: 4px; margin: 2px;">'
                f'</a>'
            )
            return Markup(html_string)
        return ""
    
    column_formatters = {
        "Portrait": lambda model, _: StudentAdmin._format_portrait(model, _, size=40),
    }

    column_details_list = [
        Student.id,
        Student.name,
        Student.version,
        Student.school,
        Student.rarity,
        Student.is_limited,
        "Portrait",
        "Artwork"
    ]

    column_formatters_detail = {
        "Portrait": lambda model, _: StudentAdmin._format_portrait(model, _, size=80),
        "Artwork": lambda model, _: StudentAdmin._format_artwork(model, _, size=80),
    }

class VersionAdmin(ModelView, model=Version):
    name = "Version"
    name_plural = "Versions"
    icon = "fa-solid fa-shirt"
    column_list = ["id", "name"]
    column_searchable_list = ["name"]

class SchoolAdmin(ModelView, model=School):
    name = "School"
    name_plural = "Schools"
    icon = "fa-solid fa-school"
    column_list = ["id", "name"]

class GachaBannerAdmin(ModelView, model=GachaBanner):
    name = "Banner"
    name_plural = "Banners"
    icon = "fa-solid fa-bullhorn"
    column_list = ["id", "banner_image", "banner_name", "preset", "included_versions", "Pickups", "Excluded"]

    @staticmethod
    def _format_pickups(model: GachaBanner, _, size: int = 40) -> Markup:
        """
        A reusable static method to generate the HTML for pickup student images.
        Takes an optional 'size' argument for flexibility.
        """
        html_string = ''.join(
            f'<a href="/admin/student/details/{student.id}" title="{student}">'
            f'  <img src="/image/student/{student.id}/portrait" width="{size}" style="border-radius: 4px; margin: 2px;">'
            f'</a>'
            for student in model.pickup_students if student.asset
        )
        return Markup(html_string)
    
    @staticmethod
    def _format_excluded(model: GachaBanner, _, size: int = 40) -> Markup:
        """
        A reusable static method to generate the HTML for pickup student images.
        Takes an optional 'size' argument for flexibility.
        """
        html_string = ''.join(
            f'<a href="/admin/student/details/{student.id}" title="{student}">'
            f'  <img src="/image/student/{student.id}/portrait" width="{size}" style="border-radius: 4px; margin: 2px;">'
            f'</a>'
            for student in model.excluded_students if student.asset
        )
        return Markup(html_string)

    column_formatters = {
        "banner_image": lambda model, _: Markup(
            f'<img src="/image/banner/{model.id}" width="120">' # Assumes you create this endpoint
        ) if model.image_data else "",

        "Pickups": lambda model, _: GachaBannerAdmin._format_pickups(model, _, size=40),
        "Excludes": lambda model, _: GachaBannerAdmin._format_excluded(model, _, size=40),
    }

    column_details_list = [
        GachaBanner.id,
        GachaBanner.name,
        GachaBanner.preset,
        GachaBanner.include_limited,
        GachaBanner.included_versions,
        "Pickups",
        "Excludes"
    ]

    column_formatters_detail = {
        "Pickups": lambda model, _: GachaBannerAdmin._format_pickups(model, _, size=60),
        "Excludes": lambda model, _: GachaBannerAdmin._format_excluded(model, _, size=60),
    }

    form_columns = [
        GachaBanner.name,
        GachaBanner.preset,
        GachaBanner.include_limited,
        GachaBanner.included_versions,
        GachaBanner.pickup_students,
        GachaBanner.excluded_students,
    ]

class GachaPresetAdmin(ModelView, model=GachaPreset):
    name = "Preset"
    name_plural = "Presets"
    icon = "fa-solid fa-cogs"
    column_list = ["id", "name", "pickup_rate", "r3_rate", "r2_rate", "r1_rate"]

class AchievementAdmin(ModelView, model=Achievement):
    name = "Achievement"
    name_plural = "Achievements"
    icon = "fa-solid fa-trophy"
    column_list = ["id", "Icon", "category", "name", "description", "key"]

    @staticmethod
    def _format_icon(model: Achievement, _, size: int = 100) -> Markup:
        if model and model.image_data:
            html_string = (
                f'<a href="/admin/achievement/details/{model.id}" title="{model}">'
                f'  <img src="/image/achievement/{model.id}" width="{size}" style="border-radius: 4px; margin: 2px;">'
                f'</a>'
            )
            return Markup(html_string)
        return ""
    
    column_formatters = {
        "Icon": lambda model, _: AchievementAdmin._format_icon(model, _, size=100),
    }

class UserAchievementAdmin(ModelView, model=UnlockAchievement):
    name = "Unlocked Achievement"
    name_plural = "Unlocked Achievements"
    icon = "fa-solid fa-lock-open"
    column_list = ["unlock_id", "unlock_on", "user", "achievement"]

class UserInventoryAdmin(ModelView, model=UserInventory):
    name = "Inventory"
    name_plural = "Inventories"
    icon = "fa-solid fa-box-archive"
    column_list = ["inventory_id", "user", "Portrait", "student", "inventory_num_obtained", "inventory_first_obtained_on", "First obtain (local time)"]
    column_searchable_list = ["user.username"]

    @staticmethod
    def _format_portrait(model: UserInventory, _, size: int = 40) -> Markup:
        student = model.student
        if student and student.asset:
            html_string = (
                f'<a href="/admin/student/details/{student.id}" title="{student}">'
                f'  <img src="/image/student/{student.id}/portrait" width="{size}" style="border-radius: 4px; margin: 2px;">'
                f'</a>'
            )
            return Markup(html_string)
        return ""
    
    column_formatters = {
        "Portrait": lambda model, _: UserInventoryAdmin._format_portrait(model, _, size=40),
        "First obtain (local time)": lambda model, _: format_datetime_as_local(model, "inventory_first_obtained_on"),
    }

class GachaTransactionAdmin(ModelView, model=GachaTransaction):
    name = "Transaction"
    name_plural = "Transactions"
    icon = "fa-solid fa-receipt"
    column_list = ["transaction_id", "user", "Portrait", "student", "transaction_create_on", "create_on (local time)"]

    @staticmethod
    def _format_portrait(model, _, size: int = 40) -> Markup:
        student = model.student
        if student and student.asset:
            html_string = (
                f'<a href="/admin/student/details/{student.student_id}" title="{student}">'
                f'  <img src="/image/student/{student.student_id}/portrait" width="{size}" style="border-radius: 4px; margin: 2px;">'
                f'</a>'
            )
            return Markup(html_string)
        return ""

    column_formatters = {
        "Portrait": lambda model, _: GachaTransactionAdmin._format_portrait(model, _, size=40),
        "create_on (local time)": lambda model, _: format_datetime_as_local(model, "transaction_create_on"),
    }
    
# --- 3. Create the Initialization Function ---
def init_admin(app: FastAPI):
    """Creates and mounts the SQLAdmin interface to the FastAPI app."""
    
    # Instantiate the authentication backend
    authentication_backend = AdminAuth(secret_key="a_very_secure_secret_key_for_sessions")
    
    # Create the Admin instance
    admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
    
    # Add all the model views
    admin.add_view(RoleAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(StudentAdmin)
    admin.add_view(VersionAdmin)
    admin.add_view(SchoolAdmin)
    admin.add_view(GachaPresetAdmin)
    admin.add_view(GachaBannerAdmin)
    admin.add_view(AchievementAdmin)
    admin.add_view(UserAchievementAdmin)
    admin.add_view(UserInventoryAdmin)
    admin.add_view(GachaTransactionAdmin)