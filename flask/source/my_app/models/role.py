from functools import wraps
from flask import abort
from flask_login import current_user
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR

from my_app import db

class Role(db.Model):
    __tablename__ = "roles"
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="역할 식별 값"
    )
    name = Column(
        VARCHAR(length=10),
        unique=True,
        nullable=False,
        comment="역할"
    )

    def __init__(self, name:str):
        self.name = name

    def __repr__(self):
        return f"Role(name='{self.name}')"

def role_required(roles:list):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_roles = [role.name for role in current_user.roles]
            for role in roles:
                if role in user_roles:
                    return f(*args, **kwargs)
            return abort(code=403)
        return decorated_function
    return decorator