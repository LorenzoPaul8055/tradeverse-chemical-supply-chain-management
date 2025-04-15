import os
from app.config import Config

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session and CSRF protection
    SECRET_KEY = 'root'

    # MySQL Database configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/tradeverse_chemical'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload configuration (for SDS, chemical labels, etc.)
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}

    # Pagination configuration
    ITEMS_PER_PAGE = 10
