from flask import abort
from flask_login import UserMixin, current_user
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

from my_app import db

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="사용자 식별 값"
    )
    username = Column(
        VARCHAR(length=50),
        unique=True,
        nullable=False,
        comment="사용자 아이디"
    )
    password = Column(
        VARCHAR(length=255),
        nullable=False,
        comment="사용자 비밀번호"
    )
    roles = relationship(
        argument="Role",
        secondary="user_roles",
        backref=backref(name="users", lazy=True),
        uselist=True
    )

    def __init__(self, username:str, password:str, roles:list):
        self.username = username
        self.password = generate_password_hash(password=password)
        self.roles = roles

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, role={self.roles})"

    def check_password(self, password:str):
        return check_password_hash(self.password, password)
    
    def serialize(self):
        user_info = {c.name: getattr(self, c.name) for c in self.__table__.columns if not c.name == "password"}
        role_info = [role.name for role in self.roles]
        user_info["roles"] = role_info
        return user_info

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

    def __repr__(self):
        return f"Role(name='{self.name}')"
    
class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="사용자 역할 매핑 식별 값"
    )
    user_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="users.id", ondelete="CASCADE"),
        nullable=False,
        comment="사용자 식별 값"
    )
    role_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="roles.id", ondelete="CASCADE"),
        nullable=False,
        comment="역할 식별 값"
    )

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