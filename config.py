import secrets
import os

basedir = os.path.abspath(os.path.dirname(__file__))
uri = os.getenv("DATABASE_URL")  # or other relevant config var
print('os.getenv:URL = {}'.format(uri))
uri = os.environ['DATABASE_URL']
print('os.environ:URL = {}'.format(uri))
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
print('URL = {}>'.format(uri))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    SECRET_KEY = "rly dont care about this now"
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = uri


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/learning_platform'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://namesEnded:OeG0YLSTVEK9@ep-steep-glitter-227283.eu-central-1.aws.neon.tech/neondb'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://yvjohiyh:cpbx7_yT0D0W3BzAUcpJfvunNplj-CRW@mouse.db.elephantsql.com/yvjohiyh'



class TestingConfig(Config):
    TESTING = True
