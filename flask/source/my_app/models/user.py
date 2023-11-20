import re
from flask import abort
from flask_wtf import FlaskForm
from flask_login import UserMixin, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

from my_app import db, lm, app

class UsernameFilter:
    def __init__(self, banned:list, regex:str, message=None):
        self.banned = banned
        self.regex = regex
        
        if not message:
            message = "사용할 수 없는 아이디입니다."
        self.message = message

    def __call__(self, form, field):
        for ban in self.banned:
            if ban in field.data.lower():
                raise ValidationError(self.message)
        
        if not re.match(re.compile(self.regex), field.data):
            raise ValidationError(self.message)
    
class LoginForm(FlaskForm):
    username = StringField(
        label="아이디",
        validators=[
            DataRequired(message="아이디를 입력하세요."),
            Length(max=10, message="로그인에 실패하였습니다."),
            UsernameFilter(banned=[], regex=r"^[a-z0-9_]*$")
        ]
    )
    password = PasswordField(
        label="비밀번호",
        validators=[
            DataRequired(message="비밀번호를 입력하세요."),
            Length(max=15, message="로그인에 실패하였습니다.")
        ]
    )
    submit = SubmitField("로그인")

class RegistrationForm(FlaskForm):
    username = StringField(
        label="아이디",
        validators=[
            DataRequired(message="아이디를 입력하세요."),
            Length(min=4, max=10, message="아이디는 4자 이상, 15자 이하여야 합니다."),
            UsernameFilter(banned=["admin"], regex=r"^[a-z0-9_]*$")
        ],
        render_kw={"id": "registerUsername"}
    )
    password = PasswordField(
        label="비밀번호",
        validators=[
            DataRequired(message="비밀번호를 입력하세요."),
            Length(min=8, max=15, message="비밀번호는 8자 이상, 15자 이하여야 합니다."),
            EqualTo(fieldname="password_confirm", message="비밀번호가 일치하지 않습니다.")
        ],
        render_kw={"id": "registerPassword"}
    )
    password_confirm = PasswordField(
        label="비밀번호 확인",
        validators=[
            DataRequired(message="비밀번호 확인을 입력하세요."),
            Length(min=8, max=15, message="비밀번호는 8자 이상, 15자 이하여야 합니다.")
        ],
        render_kw={"id": "registerPasswordConfirm"}
    )
    submit = SubmitField(
        label="회원가입",
        render_kw={"id": "registerSubmit"}
    )

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
        backref=backref(name="users", lazy=True)
    )

    def __init__(self, username:str, password:str, roles:list):
        self.username = username
        self.password = generate_password_hash(password=password)
        self.roles = roles

    def __repr__(self):
        return f"User(id='{self.id}', username='{self.username}', role={self.roles})"

    def check_password(self, password:str):
        return check_password_hash(self.password, password)
    
    def serialize(self):
        user_info = {c.name: getattr(self, c.name) for c in self.__table__.columns if not c.name == "password"}
        role_info = [role.name for role in self.roles]
        user_info["roles"] = role_info
        return user_info

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="사용자 역할 매핑 식별 값"
    )
    user_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="users.id", ondelete="CASCADE"),
        comment="사용자 식별 값"
    )
    role_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="roles.id", ondelete="CASCADE"),
        comment="역할 식별 값"
    )
    
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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