import os

class Config:
    SECRET_KEY = 'very-secret-key'  # Замени на свой
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
