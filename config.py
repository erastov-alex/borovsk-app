import os

os.environ["FLASK_APP"] = "app.py"

SECRET_KEY = "admin1234"
DATABASE_PATH = "database2.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"

SQLALCHEMY_TRACK_MODIFICATIONS = False

CACHE_TYPE = "simple"

JWT_SECRET_KEY = "BASE"

MAIL = '' #only yandex

MAIL_PASSWORD = ''

REAL_DB_PATH = os.path.join('instance', 'database2.db')
