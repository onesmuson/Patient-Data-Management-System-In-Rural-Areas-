from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# ----------------------------
# IMPORT MODELS
# ----------------------------
from models import User, Patient


# ----------------------------
# HOME PAGE
# ----------------------------
@app.route('/')
def home():
    return redirect(url_for('login'))


# ----------------------------
# REGISTER USER
# ----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Try logging in.", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        new_user = User(fullname=fullname, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


# ----------------------------
# LOGIN
# ----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['fullname'] = user.fullname
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect email or password!", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')


# ----------------------------
# LOGOUT
# ----------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))


# ----------------------------
# DASHBOARD
# ----------------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    patients = Patient.query.all()

    return render_template('dashboard.html', patients=patients, fullname=session['fullname'])


# ----------------------------
# ADD PATIENT
# ----------------------------
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        fullname = request.form['fullname']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        phone = request.form['phone']
        symptoms = request.form['symptoms']

        new_patient = Patient(
            fullname=fullname,
            age=age,
            gender=gender,
            address=address,
            phone=phone,
            symptoms=symptoms,
            created_at=datetime.utcnow()
        )

        db.session.add(new_patient)
        db.session.commit()

        flash("Patient added successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('add_patient.html')


# ----------------------------
# VIEW PATIENT
# ----------------------------
@app.route('/patient/<int:id>')
def patient(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(id)
    return render_template('patient.html', patient=patient)


# ----------------------------
# DELETE PATIENT
# ----------------------------
@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()

    flash("Patient deleted successfully!", "danger")
    return redirect(url_for('dashboard'))


# ----------------------------
# UPDATE PATIENT
# ----------------------------
@app.route('/update_patient/<int:id>', methods=['GET', 'POST'])
def update_patient(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        patient.fullname = request.form['fullname']
        patient.age = request.form['age']
        patient.gender = request.form['gender']
        patient.address = request.form['address']
        patient.phone = request.form['phone']
        patient.symptoms = request.form['symptoms']

        db.session.commit()

        flash("Patient updated successfully!", "success")
        return redirect(url_for('patient', id=id))

    return render_template('update_patient.html', patient=patient)


# ----------------------------
# REQUIRED FOR PYTHONANYWHERE
# ----------------------------
if __name__ == "__main__":
    app.run()
