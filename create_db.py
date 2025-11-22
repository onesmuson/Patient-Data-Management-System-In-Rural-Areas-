from app import app, db
from models import User
import os

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created successfully.")

    # Optional: create admin user if environment variables are set
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if admin_username and admin_password:
        if not User.query.filter_by(username=admin_username).first():
            admin = User(username=admin_username, role="admin")
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user '{admin_username}' created successfully.")
        else:
            print(f"Admin user '{admin_username}' already exists.")
    else:
        print("ADMIN_USERNAME and ADMIN_PASSWORD environment variables not set.")
