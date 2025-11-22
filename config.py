import os

class Config:
    # Secret key for Flask sessions
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")

    # MySQL database settings (PythonAnywhere)
    MYSQL_USER = "Onesmus"  # your PythonAnywhere username
    MYSQL_PASSWORD = "YOUR_DB_PASSWORD"  # replace with your actual MySQL password
    MYSQL_HOST = "Onesmus.mysql.pythonanywhere-services.com"
    MYSQL_DB = "Onesmus$default"

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

    # Avoid warnings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
