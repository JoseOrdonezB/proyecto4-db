import os

class Config:
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASS = os.environ.get('DB_PASS', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', 'db')  # OJO: nombre del contenedor del servicio de DB
    DB_NAME = os.environ.get('DB_NAME', 'ecommerce')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"