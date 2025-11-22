import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ----------------------------
# IMPORT MODELS AND CONFIG
# ----------------------------
from models import db, User, Patient, MedicalHistory, Appointment, Bill
from config import Config

# ----------------------------
# FLASK APP SETUP
# ----------------------------
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# ----------------------------
# AUTO DB + ADMIN CREATION
# ----------------------------
@app.before_first_request
def initialize_database():
    db.create_all()
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if admin_username and admin_password:
        if not User.query.filter_by(username=admin_username).first():
            admin = User(username=admin_username, role="admin")
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print("Admin created automatically")
        else:
            print("Admin already exists")
    else:
        print("ADMIN_USERNAME / ADMIN_PASSWORD not set")

# ----------------------------
# ROUTES
# ----------------------------
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect("/dashboard")
        flash("Invalid login credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect("/register")
        user = User(username=username, role="staff")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully", "success")
        return redirect("/login")
    return render_template("register.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form["username"]
        new_pass = request.form["new_password"]
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("User not found", "danger")
            return redirect("/forgot-password")
        user.set_password(new_pass)
        db.session.commit()
        flash("Password reset successfully", "success")
        return redirect("/login")
    return render_template("forgot_password.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

# ----------------------------
# PATIENT CRUD
# ----------------------------
@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        patient = Patient(
            name=request.form["name"],
            gender=request.form["gender"],
            age=request.form["age"],
            phone=request.form["phone"],
            address=request.form["address"],
            condition=request.form["condition"],
            date_registered=datetime.now(),
        )
        db.session.add(patient)
        db.session.commit()
        flash("Patient added successfully", "success")
        return redirect("/view_patients")
    return render_template("add_patient.html")

@app.route("/view_patients")
def view_patients():
    return render_template("view_patients.html", patients=Patient.query.all())

# ----------------------------
# MEDICAL HISTORY
# ----------------------------
@app.route("/add_medical_history/<int:patient_id>", methods=["GET", "POST"])
def add_medical_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == "POST":
        history = MedicalHistory(
            patient_id=patient_id,
            details=request.form["details"],
            date_added=datetime.now()
        )
        db.session.add(history)
        db.session.commit()
        flash("Medical history added", "success")
        return redirect(f"/view_medical_history/{patient_id}")
    return render_template("add_medical_history.html", patient=patient)

@app.route("/view_medical_history/<int:patient_id>")
def view_medical_history(patient_id):
    return render_template(
        "view_medical_history.html",
        patient=Patient.query.get_or_404(patient_id),
        history=MedicalHistory.query.filter_by(patient_id=patient_id).all()
    )

# ----------------------------
# APPOINTMENTS
# ----------------------------
@app.route("/add_appointment/<int:patient_id>", methods=["GET", "POST"])
def add_appointment(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == "POST":
        appointment = Appointment(
            patient_id=patient_id,
            appointment_date=request.form["date"],
            description=request.form["description"]
        )
        db.session.add(appointment)
        db.session.commit()
        flash("Appointment added", "success")
        return redirect(f"/view_appointments/{patient_id}")
    return render_template("add_appointment.html", patient=patient)

@app.route("/view_appointments/<int:patient_id>")
def view_appointments(patient_id):
    return render_template(
        "view_appointments.html",
        patient=Patient.query.get_or_404(patient_id),
        appointments=Appointment.query.filter_by(patient_id=patient_id).all()
    )

# ----------------------------
# BILLING
# ----------------------------
@app.route("/add_bill/<int:patient_id>", methods=["GET", "POST"])
def add_bill(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == "POST":
        bill = Bill(
            patient_id=patient_id,
            amount=request.form["amount"],
            description=request.form["description"],
            date=datetime.now()
        )
        db.session.add(bill)
        db.session.commit()
        flash("Bill added successfully", "success")
        return redirect(f"/view_bills/{patient_id}")
    return render_template("add_bill.html", patient=patient)

@app.route("/view_bills/<int:patient_id>")
def view_bills(patient_id):
    return render_template(
        "view_bills.html",
        patient=Patient.query.get_or_404(patient_id),
        bills=Bill.query.filter_by(patient_id=patient_id).all()
    )

# ----------------------------
# RUN APP
# ----------------------------
if __name__ == "__main__":
    app.run()
