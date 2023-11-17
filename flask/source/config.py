import os
import secrets

class Config:
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = secrets.token_bytes(nbytes=16)

    # DATABASE
    db_ip = os.environ["MARIADB_HOST"]
    db_pt = os.environ["MARIADB_PORT"]
    db_id = os.environ["MARIADB_USER"]
    db_pw = os.environ["MARIADB_PASSWORD"]
    db_nm = os.environ["MARIADB_DATABASE"]
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_id}:{db_pw}@{db_ip}:{db_pt}/{db_nm}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "8846fb3651e8f2b6f4c61a3fa4fab7e6"

config  = {
    "development"   : DevelopmentConfig,
    "production"    : ProductionConfig
}