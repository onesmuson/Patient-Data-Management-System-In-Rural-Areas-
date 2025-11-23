from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Models
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    medical_history = db.Column(db.Text)

# Routes
@app.route('/')
def dashboard():
    total_patients = Patient.query.count()
    patients = Patient.query.all()
    return render_template('dashboard.html', total_patients=total_patients, patients=patients)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        history = request.form['history']
        new_patient = Patient(name=name, age=age, medical_history=history)
        db.session.add(new_patient)
        db.session.commit()
        flash("Patient added successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('add_patient.html')

@app.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.medical_history = request.form['history']
        db.session.commit()
        flash("Patient updated successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('edit_patient.html', patient=patient)

@app.route('/delete_patient/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash("Patient deleted successfully!", "danger")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
