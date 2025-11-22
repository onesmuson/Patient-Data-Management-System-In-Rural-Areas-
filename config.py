import os

class Config:
    # Secret key for session management
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")  

    # MySQL database credentials
    MYSQL_USER = os.getenv("MYSQLUSER")       # e.g., 'yourusername'
    MYSQL_PASS = os.getenv("MYSQLPASSWORD")   # e.g., 'yourpassword'
    MYSQL_HOST = os.getenv("MYSQLHOST")       # e.g., 'yourusername.mysql.pythonanywhere-services.com'
    MYSQL_DB   = os.getenv("MYSQLDATABASE")   # e.g., 'yourusername$patient_db'

    # Construct the SQLAlchemy Database URI
    if all([MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_DB]):
        # Use MySQL Connector
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}/{MYSQL_DB}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = None  # prevents app from starting without credentials

    # Standard SQLAlchemy setting
    SQLALCHEMY_TRACK_MODIFICATIONS = False
