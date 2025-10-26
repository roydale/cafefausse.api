import os

class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///cafe_fausse.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres@localhost:5432/cafe_fausse'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'password': 'P@$$w0rd'}
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = '*'