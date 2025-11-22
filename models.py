from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# ----------------------------
# USER MODEL
# ----------------------------
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="staff")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ----------------------------
# PATIENT MODEL
# ----------------------------
class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(50))
    address = db.Column(db.String(200))
    condition = db.Column(db.String(200))
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)

    medical_history = db.relationship("MedicalHistory", backref="patient", cascade="all, delete-orphan")
    appointments = db.relationship("Appointment", backref="patient", cascade="all, delete-orphan")
    bills = db.relationship("Bill", backref="patient", cascade="all, delete-orphan")

# ----------------------------
# MEDICAL HISTORY MODEL
# ----------------------------
class MedicalHistory(db.Model):
    __tablename__ = "medical_history"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    details = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# ----------------------------
# APPOINTMENT MODEL
# ----------------------------
class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)

# ----------------------------
# BILL MODEL
# ----------------------------
class Bill(db.Model):
    __tablename__ = "bills"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
