import os
import logging
import logging.handlers
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_socketio import SocketIO
from redis import StrictRedis

from config import config

def app_logger_test(app:Flask):
    app.logger.debug(msg="debug log1") # 10
    app.logger.info(msg="info log1") # 20
    app.logger.warn(msg="warn log1") # 30
    app.logger.warning(msg="warning log1") # 30
    app.logger.error(msg="error log1") # 40
    app.logger.critical(msg="critical log1") # 50

    app.logger.setLevel(logging.DEBUG)
    app.logger.debug(msg="debug log2")
    app.logger.info(msg="info log2")

app     = Flask(import_name=__name__)
app_logger_test(app)
db      = SQLAlchemy()
lm      = LoginManager()
jwt     = JWTManager()
cache   = Cache()
sock    = SocketIO()
rc      = StrictRedis(host="redis", port=6379, db=0)
logger  = logging.getLogger("myLogger")

def create_app():
    app.config.from_object(obj=config["development"])

    with app.app_context():
        from my_app.views.index import bp_index
        from my_app.views.board import bp_board
        from my_app.views.comment import bp_comment
        from my_app.views.dashboard import bp_dashboard
        from my_app.views.cache import bp_cache
        from my_app.api.v1 import bp_api

        app.register_blueprint(blueprint=bp_index)
        app.register_blueprint(blueprint=bp_board)
        app.register_blueprint(blueprint=bp_comment)
        app.register_blueprint(blueprint=bp_dashboard)
        app.register_blueprint(blueprint=bp_cache)
        app.register_blueprint(blueprint=bp_api)

        db.init_app(app=app)
        db.create_all()

        lm.login_view       = "index.login"
        lm.login_message    = "로그인이 필요합니다."
        lm.init_app(app=app)

        jwt.init_app(app=app)

        cache.init_app(app=app)
        cache.clear()

        sock.init_app(app=app)

        # logging.getLogger("werkzeug").disabled = True
        # logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] [%(levelname)s] [%(remote_addr)s] \"%(method)s %(url)s %(version)s\" : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        if not os.path.isdir(s=app.config.get("LOG_DIR")):
            os.mkdir(path=app.config.get("LOG_DIR"))
        
        log_path = os.path.join(app.config.get("LOG_DIR"), app.config.get("LOG_FILE"))
        # handler = logging.FileHandler(filename=log_path, mode="a", encoding="utf-8")
        handler = logging.handlers.RotatingFileHandler(filename=log_path, mode="a", encoding="utf-8", maxBytes=200, backupCount=3)
        handler.setFormatter(fmt=logging.Formatter('[%(asctime)s] [%(levelname)s] [%(remote_addr)s] \"%(method)s %(url)s %(version)s\" : %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        return app
    
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    """
    사용된 액세스 토큰(access_token)의 재사용을 방지합니다.
    """

    if not jwt_payload and "jti" not in jwt_payload:
        return None
    
    jti = jwt_payload.get("jti")
    token = rc.get(name=jti)
    return token is not None