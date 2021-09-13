import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI=''

class Prod(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''

class Dev(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    project_dir = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(project_dir, "lmsdb.db"))

class Test(Config):
    TESTING = True
    project_dir = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(project_dir, "test.db"))