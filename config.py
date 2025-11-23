import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")

    MYSQL_USER = "Onesmuson"
    MYSQL_PASSWORD = "Admin123"
    MYSQL_HOST = "Onesmuson.mysql.pythonanywhere-services.com"
    MYSQL_DB = "Onesmuson$default"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
