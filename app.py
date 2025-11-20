from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Patient, MedicalHistory, Appointment, Bill
from config import Config
from datetime import datetime
import os

# -------------------------
# Flask App Initialization
# -------------------------
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# -------------------------
# Home Route
# -------------------------
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# -------------------------
# Authentication Module
# -------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# -------------------------
# Dashboard
# -------------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template(
        'dashboard.html',
        patient_count=Patient.query.count(),
        appointment_count=Appointment.query.count(),
        bill_count=Bill.query.count()
    )

# -------------------------
# Patient Management
# -------------------------
@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        patient = Patient(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            dob=datetime.strptime(request.form['dob'], '%Y-%m-%d'),
            gender=request.form['gender'],
            allergies=request.form['allergies'],
            medical_notes=request.form['medical_notes']
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully', 'success')
        return redirect(url_for('view_patients'))
    return render_template('add_patient.html')

@app.route('/patients')
def view_patients():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    patients = Patient.query.all()
    return render_template('view_patients.html', patients=patients)

# -------------------------
# Medical History
# -------------------------
@app.route('/patients/<int:patient_id>/history/add', methods=['GET', 'POST'])
def add_medical_history(patient_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(patient_id)

    if request.method == 'POST':
        history = MedicalHistory(
            patient_id=patient.id,
            symptoms=request.form['symptoms'],
            diagnosis=request.form['diagnosis'],
            prescribed_drug=request.form['prescribed_drug']
        )
        db.session.add(history)
        db.session.commit()
        flash('Medical history added', 'success')
        return redirect(url_for('view_patient_history', patient_id=patient.id))

    return render_template('add_medical_history.html', patient=patient)

@app.route('/patients/<int:patient_id>/history')
def view_patient_history(patient_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(patient_id)
    histories = MedicalHistory.query.filter_by(patient_id=patient.id).all()
    return render_template('view_medical_history.html', patient=patient, histories=histories)

# -------------------------
# Appointments
# -------------------------
@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    patients = Patient.query.all()

    if request.method == 'POST':
        appointment = Appointment(
            patient_id=request.form['patient_id'],
            doctor_name=request.form['doctor_name'],
            appointment_date=datetime.strptime(request.form['appointment_date'], '%Y-%m-%dT%H:%M'),
            status='Scheduled'
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment scheduled', 'success')
        return redirect(url_for('view_appointments'))

    return render_template('add_appointment.html', patients=patients)

@app.route('/appointments')
def view_appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    appointments = Appointment.query.all()
    return render_template('view_appointments.html', appointments=appointments)

# -------------------------
# Billing
# -------------------------
@app.route('/billing/add', methods=['GET', 'POST'])
def add_bill():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    patients = Patient.query.all()

    if request.method == 'POST':
        bill = Bill(
            patient_id=request.form['patient_id'],
            total_amount=float(request.form['total_amount'])
        )
        db.session.add(bill)
        db.session.commit()
        flash('Bill created', 'success')
        return redirect(url_for('view_bills'))

    return render_template('add_bill.html', patients=patients)

@app.route('/billing')
def view_bills():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    bills = Bill.query.all()
    return render_template('view_bills.html', bills=bills)

# -------------------------
# Reports
# -------------------------
@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template(
        'reports.html',
        patient_count=Patient.query.count(),
        appointment_count=Appointment.query.count(),
        bill_count=Bill.query.count()
    )

# -------------------------
# Run App
# -------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ensure tables exist
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
