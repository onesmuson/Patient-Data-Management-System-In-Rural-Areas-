"""
create_db.py
Creates database tables and a default admin user.
Run locally: python create_db.py
Or run in Render shell after DATABASE_URL is set.
"""
import os
from werkzeug.security import generate_password_hash
from models import db, User
from app import app

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@123')  # change in production

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username=ADMIN_USERNAME).first():
        admin = User(
            username=ADMIN_USERNAME,
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            role='Admin'
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Created admin user: {ADMIN_USERNAME}")
    else:
        print(f"Admin user '{ADMIN_USERNAME}' already exists.")
    print("Database tables created/verified successfully.")
