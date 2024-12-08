import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # Render's database URL from environment variables
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable FS monitoring for performance
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Set your secret key
