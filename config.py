import os

class Config:
    # Secret key for Flask sessions
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")

    # MySQL database settings
    MYSQL_USER = "Onesmuson"
    MYSQL_PASSWORD = "Admin123"  # your new MySQL password
    MYSQL_HOST = "Onesmuson.mysql.pythonanywhere-services.com"
    MYSQL_DB = "Onesmuson$default"

    # SQLAlchemy URI
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
