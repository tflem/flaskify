import os

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
             'postgresql+psycopg2://postgres:Fa37PhAn@localhost/flaskify_db')
    print SQLALCHEMY_DATABASE_URI       

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}