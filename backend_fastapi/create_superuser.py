from .util.database import SessionLocal, engine
from .util.models import User, Role # <-- Add Role
from .util.auth import get_password_hash
import argparse

def main():
    # ... (argparse setup is the same)
    parser = argparse.ArgumentParser(description="Create a new user for the application.")
    parser.add_argument("username", type=str, help="The username for the new user.")
    parser.add_argument("password", type=str, help="The password for the new user.")
    parser.add_argument(
        "--role",
        type=str,
        default="superuser",
        choices=["member", "superuser"],
        help="The role to assign to the user (default: superuser)."
    )
    args = parser.parse_args()


    print(f"Attempting to create user '{args.username}' with role '{args.role}'...")

    with SessionLocal() as db:
        # Check if user already exists
        if db.query(User).filter(User.username == args.username).first():
            print(f"Error: User '{args.username}' already exists.")
            return

        # --- START OF CHANGES ---
        # Find the role object in the database
        role_obj = db.query(Role).filter(Role.role_name == args.role).first()
        if not role_obj:
            print(f"Error: Role '{args.role}' does not exist in the database.")
            print("Please ensure roles are seeded correctly (e.g., 'member', 'superuser').")
            return
        # --- END OF CHANGES ---

        hashed_password = get_password_hash(args.password)

        new_user = User(
            username=args.username,
            hashed_password=hashed_password,
            role_id_fk=role_obj.role_id # <-- Use the foreign key ID
        )

        db.add(new_user)
        db.commit()

        print(f"Successfully created user '{args.username}' with role '{args.role}'.")

if __name__ == "__main__":
    main()