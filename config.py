import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    MYSQL_USER = os.getenv("MYSQL_USER", "Onesmuson")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Admin1234")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "Onesmuson.mysql.pythonanywhere-services.com")
    MYSQL_DB = os.getenv("MYSQL_DB", "Onesmuson$default")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
