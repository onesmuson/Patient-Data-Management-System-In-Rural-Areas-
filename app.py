from flask import Flask, render_template, request, redirect, url_for
from models import db, Patient  # Assuming you are using SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/pdms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        # Save patient logic
        return redirect(url_for('view_patients'))
    return render_template('add_patient.html')

@app.route('/patients')
def view_patients():
    # Fetch patients from DB
    return render_template('view_patients.html')

@app.route('/reports')
def reports():
    # Generate reports
    return render_template('reports.html')

if __name__ == "__main__":
    app.run(debug=True)
