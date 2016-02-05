

class Config(object):
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
