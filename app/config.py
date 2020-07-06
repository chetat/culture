
# Define the application directory
import os
from dotenv import load_dotenv
from pathlib import Path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config(object):
    # Signal application everytime there is a change in Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    SECRET_KEY = os.environ["SECRET_KEY"]


class DevelopmentConfig(Config):
    # Statement for enabling the development environment
    ENV = "development"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')
