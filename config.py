import os
from dotenv import load_dotenv

"""
MAIL 
MAIL_PASSWORD 
JWT_SECRET_KEY 
SECRET_KEY
values in settings.env
"""

load_dotenv(dotenv_path="settings.env")

os.environ["FLASK_APP"] = "app.py"
DATABASE_PATH = "database2.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
CACHE_TYPE = "simple"
REAL_DB_PATH = os.path.join('instance', DATABASE_PATH)
SMTP_SERVER = 'server190.hosting.reg.ru'
SMTP_PORT = 587
