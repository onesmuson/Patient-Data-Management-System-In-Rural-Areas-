import os

class Config:
    """
    Configuration for Flask app with MySQL database
    """

    # Secret key for sessions and Flask security
    SECRET_KEY = os.getenv("SECRET_KEY", "your_strong_fallback_secret_key")

    # MySQL database connection URI
    # Format: mysql+mysqlconnector://USERNAME:PASSWORD@HOST/DATABASE
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://Onesmuson:YOUR_DB_PASSWORD@Onesmuson.mysql.pythonanywhere-services.com/Onesmus$default"

    # Disable SQLAlchemy event system to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
