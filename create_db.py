from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import os

print("Using database URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database tables created successfully.")

    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    if User.query.filter_by(username=admin_username).first():
        print(f"Admin user '{admin_username}' already exists.")
    else:
        admin = User(username=admin_username, role="admin")
        admin.password_hash = generate_password_hash(admin_password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{admin_username}' created successfully with password '{admin_password}'.")
