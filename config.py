import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEFAULT_PG_LEDGER_CONNECTION_STRING = 'host=127.0.0.1 port=5432 dbname=pg_ledger user=postgres password=admin'
  
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    PG_LEDGER_CONNECTION_STRING = os.environ.get('DEV_PG_LEDGER_CONNECTION_STRING') or \
        Config.DEFAULT_PG_LEDGER_CONNECTION_STRING

class TestingConfig(Config):
    TESTING = True
    PG_LEDGER_CONNECTION_STRING = os.environ.get('TEST_PG_LEDGER_CONNECTION_STRING') or \
        Config.DEFAULT_PG_LEDGER_CONNECTION_STRING

class ProductionConfig(Config):
    PG_LEDGER_CONNECTION_STRING = os.environ.get('PG_LEDGER_CONNECTION_STRING') or \
        Config.DEFAULT_PG_LEDGER_CONNECTION_STRING

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
