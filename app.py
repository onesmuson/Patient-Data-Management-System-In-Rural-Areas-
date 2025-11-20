from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, User, Patient, MedicalHistory, Appointment, Bill
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# -------------------- ROUTES --------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# ---------- Authentication ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------- Dashboard ----------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    patient_count = Patient.query.count()
    appointment_count = Appointment.query.count()
    bill_count = Bill.query.count()
    return render_template('dashboard.html', 
                           patient_count=patient_count,
                           appointment_count=appointment_count,
                           bill_count=bill_count)

# ---------- Patient Management ----------
@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        allergies = request.form['allergies']
        medical_notes = request.form['medical_notes']
        patient = Patient(first_name=first_name, last_name=last_name,
                          dob=datetime.strptime(dob, '%Y-%m-%d'),
                          gender=gender, allergies=allergies,
                          medical_notes=medical_notes)
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully', 'success')
        return redirect(url_for('view_patients'))
    return render_template('add_patient.html')

@app.route('/patients')
def view_patients():
    patients = Patient.query.all()
    return render_template('view_patients.html', patients=patients)

# ---------- Reports ----------
@app.route('/reports')
def reports():
    patient_count = Patient.query.count()
    appointment_count = Appointment.query.count()
    bill_count = Bill.query.count()
    return render_template('reports.html',
                           patient_count=patient_count,
                           appointment_count=appointment_count,
                           bill_count=bill_count)

# ---------- Run App ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
