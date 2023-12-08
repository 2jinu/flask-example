from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from werkzeug.security import check_password_hash, generate_password_hash

from my_app import db, lm

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
        secondary="rel_user_roles",
        backref=backref(name="users", lazy=True),
        uselist=True
    )
    comments = relationship(
        argument="Comment",
        secondary="rel_user_comments",
        backref=backref(name="users"),
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
    
    def is_admin(self):
        return "ADMIN" in [role.name for role in self.roles]

    def serialize(self):
        user_info = {c.name: getattr(self, c.name) for c in self.__table__.columns if not c.name == "password"}
        role_info = [role.name for role in self.roles]
        user_info["roles"] = role_info
        return user_info

@lm.user_loader
def load_user(user_id):
    return User.query.get(ident=int(user_id))

class UserRoles(db.Model):
    __tablename__ = "rel_user_roles"
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

class UserComments(db.Model):
    __tablename__ = "rel_user_comments"
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="사용자 댓글 매핑 식별 값"
    )
    user_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="users.id", ondelete="CASCADE"),
        nullable=False,
        comment="사용자 식별 값"
    )
    comment_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="comments.id", ondelete="CASCADE"),
        nullable=False,
        comment="댓글 식별 값"
    )