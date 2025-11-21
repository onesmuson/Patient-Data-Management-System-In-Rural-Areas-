import os

class Config:
    # Essential for application security and sessions
    SECRET_KEY = os.getenv("SECRET_KEY", "your_strong_fallback_secret_key") 

    # Retrieve MySQL components (matching environment variables from your dashboard)
    MYSQL_USER = os.getenv("MYSQLUSER")
    MYSQL_PASS = os.getenv("MYSQLPASSWORD")
    MYSQL_HOST = os.getenv("MYSQLHOST") 
    MYSQL_DB = os.getenv("MYSQLDATABASE") 

    # Construct the SQLAlchemy Database URI
    if all([MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_DB]):
        # Format: mysql+mysqlconnector://user:password@host/database
        # This uses the data retrieved from your environment variables.
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}/{MYSQL_DB}"
        )
    else:
        # If any essential variable is missing, the URI is set to None, 
        # which will prevent the application from starting without credentials.
        SQLALCHEMY_DATABASE_URI = None

    # Standard setting for Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
