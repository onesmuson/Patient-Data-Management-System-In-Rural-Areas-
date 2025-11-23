from app import db, Admin

db.create_all()
print("Tables created successfully!")

if not Admin.query.filter_by(username='admin').first():
    admin = Admin(username='admin')
    admin.set_password('Admin1234')
    db.session.add(admin)
    db.session.commit()
    print("Admin created: username=admin, password=Admin1234")
else:
    print("Admin already exists.")
