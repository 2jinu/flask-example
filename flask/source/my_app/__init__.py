from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import config

app     = Flask(import_name=__name__, template_folder="templates")
db      = SQLAlchemy()
lm      = LoginManager()

def create_app():
    app.config.from_object(obj=config["development"])

    with app.app_context():
        from my_app.index import bp_index
        from my_app.board import bp_board

        app.register_blueprint(blueprint=bp_index)
        app.register_blueprint(blueprint=bp_board)

        db.init_app(app=app)
        import my_app.models.user
        import my_app.models.post
        db.create_all()

        lm.login_view = "index.main"
        lm.login_message = "로그인이 필요합니다."
        lm.init_app(app=app)
        
        return app