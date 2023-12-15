import os
import secrets
import datetime

class Config:
    SECRET_KEY = secrets.token_bytes(nbytes=16)
    PROPAGATE_EXCEPTIONS = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=15)

    # DATABASE
    db_pt = os.environ["MARIADB_PORT"]
    db_id = os.environ["MARIADB_USER"]
    db_pw = os.environ["MARIADB_PASSWORD"]
    db_nm = os.environ["MARIADB_DATABASE"]
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_id}:{db_pw}@db:{db_pt}/{db_nm}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)

    # Cache
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "redis"
    CACHE_DEFAULT_TIMEOUT = 10

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "8846fb3651e8f2b6f4c61a3fa4fab7e6"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7)

config  = {
    "development"   : DevelopmentConfig,
    "production"    : ProductionConfig
}