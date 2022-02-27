import os
from configurations.base_config import BaseConfig
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(BaseConfig):
    USER = os.environ.get("DB_USER_NAME")
    DB_NAME = os.environ.get("DB_NAME")
    PASSWORD = os.environ.get("DB_PASSWORD")
    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")
    SECRET_KEY = os.environ.get("SECRET_KEY")
