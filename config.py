import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nilgiri_career_grid_secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///career_grid.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
