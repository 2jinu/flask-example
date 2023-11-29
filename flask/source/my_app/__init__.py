from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from redis import StrictRedis

from config import config

app     = Flask(import_name=__name__, template_folder="templates")
db      = SQLAlchemy()
lm      = LoginManager()
jwt     = JWTManager()
rc      = StrictRedis(host="redis", port=6379, db=0)

def create_app():
    app.config.from_object(obj=config["development"])

    with app.app_context():
        from my_app.views.index import bp_index
        from my_app.views.board import bp_board
        from my_app.api.v1 import bp_api

        app.register_blueprint(blueprint=bp_index)
        app.register_blueprint(blueprint=bp_board)
        app.register_blueprint(blueprint=bp_api)

        db.init_app(app=app)
        db.create_all()

        lm.login_view       = "index.login"
        lm.login_message    = "로그인이 필요합니다."
        lm.init_app(app=app)

        jwt.init_app(app=app)
        
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