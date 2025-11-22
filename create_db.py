import os
from app import app, db
from models import User

# ----------------------------
# CREATE DATABASE AND TABLES
# ----------------------------
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created successfully!")

    # ----------------------------
    # CREATE ADMIN USER
    # ----------------------------
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")  # Replace with a strong password

    # Check if admin already exists
    if not User.query.filter_by(username=admin_username).first():
        admin = User(username=admin_username, role="admin")
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{admin_username}' created successfully!")
    else:
        print(f"Admin user '{admin_username}' already exists.")
