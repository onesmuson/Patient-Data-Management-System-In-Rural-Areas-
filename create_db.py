from app import app, db
from models import User

# ----------------------------
# CREATE DATABASE AND TABLES
# ----------------------------
with app.app_context():
    db.create_all()
    print("All tables created successfully!")

    # ----------------------------
    # CREATE ADMIN USER
    # ----------------------------
    admin_username = "admin"  # change if you want
    admin_password = "admin123"  # change to a strong password

    if not User.query.filter_by(username=admin_username).first():
        admin = User(username=admin_username, role="admin")
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{admin_username}' created successfully!")
    else:
        print(f"Admin user '{admin_username}' already exists.")
