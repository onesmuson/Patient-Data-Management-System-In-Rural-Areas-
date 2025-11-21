import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
from models import db, User, Patient, MedicalHistory, Appointment, Bill

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.secret_key = app.config.get('SECRET_KEY', 'dev_secret_key')

# simple login_required decorator
from functools import wraps
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue', 'warning')
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        if not username or not password:
            flash('Provide username and password', 'danger')
            return redirect(url_for('register'))
        if password != confirm:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Username already in use', 'danger')
            return redirect(url_for('register'))
        user = User(username=username, password_hash=generate_password_hash(password), role='HealthWorker')
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Logged in successfully', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'success')
    return redirect(url_for('login'))

# Forgot password -> verifies username and shows reset UI
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            flash('Enter username', 'danger')
            return redirect(url_for('forgot_password'))
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('No account found with that username', 'danger')
            return redirect(url_for('forgot_password'))
        # store username in session for reset flow
        session['pw_reset_user'] = user.username
        flash('User verified. Enter new password now.', 'info')
        return redirect(url_for('reset_password'))
    return render_template('forgot_password.html')

# Reset password (on-screen)
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    username = session.get('pw_reset_user')
    if not username:
        flash('Password reset session not found. Start again.', 'warning')
        return redirect(url_for('forgot_password'))
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found', 'danger')
        session.pop('pw_reset_user', None)
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        new_pw = request.form.get('new_password', '')
        confirm = request.form.get('confirm_password', '')
        if not new_pw:
            flash('Enter a new password', 'danger')
            return redirect(url_for('reset_password'))
        if new_pw != confirm:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('reset_password'))
        user.password_hash = generate_password_hash(new_pw)
        db.session.commit()
        session.pop('pw_reset_user', None)
        flash('Password reset successful, please login.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', username=username)

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',
                           patient_count=Patient.query.count(),
                           appointment_count=Appointment.query.count(),
                           bill_count=Bill.query.count())

# Add patient
@app.route('/patients/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        dob_raw = request.form.get('dob')
        dob = datetime.strptime(dob_raw, '%Y-%m-%d').date() if dob_raw else None
        patient = Patient(
            first_name=request.form.get('first_name','').strip(),
            last_name=request.form.get('last_name','').strip(),
            dob=dob,
            gender=request.form.get('gender'),
            allergies=request.form.get('allergies'),
            medical_notes=request.form.get('medical_notes')
        )
        try:
            db.session.add(patient)
            db.session.commit()
            flash('Patient saved', 'success')
            return redirect(url_for('view_patients'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    return render_template('add_patient.html')

# View patients
@app.route('/patients')
@login_required
def view_patients():
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    return render_template('view_patients.html', patients=patients)

# Add medical history
@app.route('/patients/<int:patient_id>/history/add', methods=['GET', 'POST'])
@login_required
def add_medical_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        history = MedicalHistory(
            patient_id=patient.id,
            symptoms=request.form.get('symptoms'),
            diagnosis=request.form.get('diagnosis'),
            prescribed_drug=request.form.get('prescribed_drug'),
            allergies_note=request.form.get('allergies_note')
        )
        try:
            db.session.add(history)
            db.session.commit()
            flash('Medical history added', 'success')
            return redirect(url_for('view_medical_history', patient_id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    return render_template('add_medical_history.html', patient=patient)

# View medical history
@app.route('/patients/<int:patient_id>/history')
@login_required
def view_medical_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    histories = MedicalHistory.query.filter_by(patient_id=patient.id).order_by(MedicalHistory.created_at.desc()).all()
    return render_template('view_medical_history.html', patient=patient, histories=histories)

# Appointments
@app.route('/appointments/add', methods=['GET', 'POST'])
@login_required
def add_appointment():
    patients = Patient.query.order_by(Patient.last_name).all()
    if request.method == 'POST':
        appt_dt = datetime.strptime(request.form.get('appointment_date'), '%Y-%m-%dT%H:%M')
        appointment = Appointment(
            patient_id=int(request.form.get('patient_id')),
            doctor_name=request.form.get('doctor_name'),
            appointment_date=appt_dt,
            status='Scheduled'
        )
        try:
            db.session.add(appointment)
            db.session.commit()
            flash('Appointment scheduled', 'success')
            return redirect(url_for('view_appointments'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    return render_template('add_appointment.html', patients=patients)

@app.route('/appointments')
@login_required
def view_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('view_appointments.html', appointments=appointments)

# Billing
@app.route('/billing/add', methods=['GET', 'POST'])
@login_required
def add_bill():
    patients = Patient.query.order_by(Patient.last_name).all()
    if request.method == 'POST':
        try:
            total = float(request.form.get('total_amount','0'))
            bill = Bill(patient_id=int(request.form.get('patient_id')), total_amount=total)
            db.session.add(bill)
            db.session.commit()
            flash('Bill created', 'success')
            return redirect(url_for('view_bills'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')
    return render_template('add_bill.html', patients=patients)

@app.route('/billing')
@login_required
def view_bills():
    bills = Bill.query.order_by(Bill.created_at.desc()).all()
    return render_template('view_bills.html', bills=bills)

# Reports
@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html',
                           patient_count=Patient.query.count(),
                           appointment_count=Appointment.query.count(),
                           bill_count=Bill.query.count())

# Ensure tables created at start
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
