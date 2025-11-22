from app import app, db
from models import User

# Load Flask app context
with app.app_context():
    # Create all tables
    db.create_all()
    print("✅ Database tables created successfully")

    # Get admin credentials from environment
    import os
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        print("⚠️ ADMIN_USERNAME or ADMIN_PASSWORD not set in environment variables")
    else:
        # Check if admin already exists
        existing_admin = User.query.filter_by(username=admin_username).first()
        if existing_admin:
            print("ℹ️ Admin user already exists")
        else:
            # Create admin user
            admin = User(username=admin_username, role="admin")
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(f"✅ Admin user '{admin_username}' created successfully")
