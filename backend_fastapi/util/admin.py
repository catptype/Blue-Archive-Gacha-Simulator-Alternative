from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from jose import jwt
from markupsafe import Markup

# Import your database engine and models
from .database import engine, SessionLocal
from . import models
from .auth import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token # Import secrets from your auth module
from .timezone import format_datetime_as_local
from datetime import timedelta

# --- 1. Define the Authentication Backend ---
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # This is where you would properly verify the password.
        # We need to import the verify_password function.
        from .auth import verify_password

        with SessionLocal() as db:
            user = db.query(models.User).filter(models.User.username == username).first()
            if user and verify_password(password, user.hashed_password) and user.role.role_name == "superuser":
                # Create a token for the session
                # from .auth import create_access_token
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
                user = db.query(models.User).filter(models.User.username == username).first()
                if user and user.role.role_name == "superuser":
                    return True
        except Exception:
            return False
            
        return False

# --- 2. Define the Model Views ---
# See icon at https://fontawesome.com/search?f=classic&s=solid&ic=free&o=r

class RoleAdmin(ModelView, model=models.Role):
    name = "Role"
    name_plural = "Roles"
    icon = "fa-solid fa-user-shield"
    column_list = [models.Role.role_id, models.Role.role_name]

class UserAdmin(ModelView, model=models.User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-users"
    column_list = [models.User.user_id, models.User.username, models.User.role]
    column_details_exclude_list = [models.User.hashed_password]
    form_excluded_columns = [models.User.hashed_password]

class StudentAdmin(ModelView, model=models.Student):
    name = "Student"
    name_plural = "Students"
    icon = "fa-solid fa-graduation-cap"
    column_list = ["student_id", "Portrait", "student_name", "version", "student_rarity", "school"]
    column_searchable_list = [models.Student.student_name, "school.school_name", "version.version_name"]

    @staticmethod
    def _format_portrait(model, _, size: int = 40) -> Markup:
        if model and model.asset:
            html_string = (
                f'<a href="/admin/student/details/{model.student_id}" title="{model}">'
                f'  <img src="/image/student/{model.student_id}/portrait" width="{size}" style="border-radius: 4px; margin: 2px;">'
                f'</a>'
            )
            return Markup(html_string)
        return ""
    
    column_formatters = {
        "Portrait": lambda model, _: StudentAdmin._format_portrait(model, _, size=40),
    }

class VersionAdmin(ModelView, model=models.Version):
    name = "Version"
    name_plural = "Versions"
    icon = "fa-solid fa-shirt"
    column_list = ["version_id", "version_name"]
    column_searchable_list = ["version_name"]

class SchoolAdmin(ModelView, model=models.School):
    name = "School"
    name_plural = "Schools"
    icon = "fa-solid fa-school"
    column_list = ["school_id", "school_name"]

class GachaBannerAdmin(ModelView, model=models.GachaBanner):
    name = "Banner"
    name_plural = "Banners"
    icon = "fa-solid fa-bullhorn"
    column_list = ["banner_id", "banner_image", "banner_name", "preset", "included_versions", "Pickups", "Excluded"]

    @staticmethod
    def _format_pickups(model, _, size: int = 40) -> Markup:
        """
        A reusable static method to generate the HTML for pickup student images.
        Takes an optional 'size' argument for flexibility.
        """
        html_string = ''.join(
            f'<a href="/admin/student/details/{student.student_id}" title="{student}">'
            f'  <img src="/image/student/{student.student_id}/portrait" width="{size}" style="border-radius: 4px; margin: 2px;">'
            f'</a>'
            for student in model.pickup_students if student.asset
        )
        return Markup(html_string)
    
    @staticmethod
    def _format_excluded(model, _, size: int = 40) -> Markup:
        """
        A reusable static method to generate the HTML for pickup student images.
        Takes an optional 'size' argument for flexibility.
        """
        html_string = ''.join(
            f'<a href="/admin/student/details/{student.student_id}" title="{student}">'
            f'  <img src="/image/student/{student.student_id}/portrait" width="{size}" style="border-radius: 4px; margin: 2px;">'
            f'</a>'
            for student in model.excluded_students if student.asset
        )
        return Markup(html_string)

    column_formatters = {
        "banner_image": lambda model, _: Markup(
            f'<img src="/image/banner/{model.banner_id}" width="120">' # Assumes you create this endpoint
        ) if model.banner_image else "",

        "Pickups": lambda model, _: GachaBannerAdmin._format_pickups(model, _, size=40),
        "Excludes": lambda model, _: GachaBannerAdmin._format_excluded(model, _, size=40),
    }

    column_details_list = [
        models.GachaBanner.banner_id,
        models.GachaBanner.banner_name,
        models.GachaBanner.preset,
        models.GachaBanner.banner_include_limited,
        models.GachaBanner.included_versions,
        "Pickups",
        "Excludes"
    ]

    column_formatters_detail = {
        "Pickups": lambda model, _: GachaBannerAdmin._format_pickups(model, _, size=60),
        "Excludes": lambda model, _: GachaBannerAdmin._format_excluded(model, _, size=60),
    }

    form_columns = [
        models.GachaBanner.banner_name,
        models.GachaBanner.preset,
        models.GachaBanner.banner_include_limited,
        models.GachaBanner.included_versions,
        models.GachaBanner.pickup_students,
        models.GachaBanner.excluded_students,
    ]

class GachaPresetAdmin(ModelView, model=models.GachaPreset):
    name = "Preset"
    name_plural = "Presets"
    icon = "fa-solid fa-cogs"
    column_list = ["preset_id", "preset_name", "preset_pickup_rate", "preset_r3_rate", "preset_r2_rate", "preset_r1_rate"]

class AchievementAdmin(ModelView, model=models.Achievement):
    name = "Achievement"
    name_plural = "Achievements"
    icon = "fa-solid fa-trophy"
    column_list = ["achievement_id", "Icon", "achievement_category", "achievement_name", "achievement_description", "achievement_key"]

    @staticmethod
    def _format_icon(model, _, size: int = 100) -> Markup:
        if model and model.achievement_image:
            html_string = (
                f'<a href="/admin/achievement/details/{model.achievement_id}" title="{model}">'
                f'  <img src="/image/achievement/{model.achievement_id}" width="{size}" style="border-radius: 4px; margin: 2px;">'
                f'</a>'
            )
            return Markup(html_string)
        return ""
    
    column_formatters = {
        "Icon": lambda model, _: AchievementAdmin._format_icon(model, _, size=100),
    }

class UserAchievementAdmin(ModelView, model=models.UnlockAchievement):
    name = "Unlocked Achievement"
    name_plural = "Unlocked Achievements"
    icon = "fa-solid fa-lock-open"
    column_list = ["unlock_id", "unlock_on", "user", "achievement"]

class UserInventoryAdmin(ModelView, model=models.UserInventory):
    name = "Inventory"
    name_plural = "Inventories"
    icon = "fa-solid fa-box-archive"
    column_list = ["inventory_id", "user", "Portrait", "student", "inventory_num_obtained", "inventory_first_obtained_on", "First obtain (local time)"]
    column_searchable_list = ["user.username"]

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
        "Portrait": lambda model, _: UserInventoryAdmin._format_portrait(model, _, size=40),
        "First obtain (local time)": lambda model, _: format_datetime_as_local(model, "inventory_first_obtained_on"),
    }

class GachaTransactionAdmin(ModelView, model=models.GachaTransaction):
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