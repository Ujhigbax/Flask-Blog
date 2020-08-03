import os
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '\x94A\xbc]\xb3b\xf2\x8fz\xef&!\xbe\xc3[,\xd5\xe2\xdaSR~~\x96'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data_base.db'

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False