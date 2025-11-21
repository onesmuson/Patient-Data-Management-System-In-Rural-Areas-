import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://username:password@localhost:5432/pdms_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
