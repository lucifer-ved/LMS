import os

class Config(object):
    DEBUG = False
    Testing = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Prod(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class Dev(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    project_dir = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(project_dir, "lmsdb.db"))