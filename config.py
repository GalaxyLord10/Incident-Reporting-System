class DefaultConfig:
    DEBUG = True
    SECRET_KEY = 'supersecretkey'  # For session management, ideally should be pulled from environment variables in production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///incidents.db'


class TestConfig:
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'testsupersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SESSION_COOKIE_SECURE = 'False'
