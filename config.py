import os

class Config:
    SECRET_KEY = os.urandom(24).hex()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/cafeteria.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False