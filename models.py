from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    allergies = db.Column(db.Text)
    medical_notes = db.Column(db.Text)
    medical_histories = db.relationship('MedicalHistory', backref='patient', lazy=True)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    bills = db.relationship('Bill', backref='patient', lazy=True)

class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    symptoms = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    prescribed_drug = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_name = db.Column(db.String(100))
    appointment_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Scheduled')

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    total_amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
