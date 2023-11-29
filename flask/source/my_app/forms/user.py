import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

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
        ],
        render_kw={"autofocus": True, "placeholder": ""}
    )
    password = PasswordField(
        label="비밀번호",
        validators=[
            DataRequired(message="비밀번호를 입력하세요."),
            Length(max=15, message="로그인에 실패하였습니다.")
        ],
        render_kw={"placeholder": ""}
    )
    submit = SubmitField(label="로그인")

class RegistrationForm(FlaskForm):
    username = StringField(
        label="아이디",
        validators=[
            DataRequired(message="아이디를 입력하세요."),
            Length(min=4, max=10, message="아이디는 4자 이상, 15자 이하여야 합니다."),
            UsernameFilter(banned=["admin"], regex=r"^[a-z0-9_]*$")
        ],
        render_kw={"id": "registerUsername", "autofocus": True, "placeholder": ""}
    )
    password = PasswordField(
        label="비밀번호",
        validators=[
            DataRequired(message="비밀번호를 입력하세요."),
            Length(min=8, max=15, message="비밀번호는 8자 이상, 15자 이하여야 합니다."),
            EqualTo(fieldname="password_confirm", message="비밀번호가 일치하지 않습니다.")
        ],
        render_kw={"placeholder": ""}
    )
    password_confirm = PasswordField(
        label="비밀번호 확인",
        validators=[
            DataRequired(message="비밀번호 확인을 입력하세요."),
            Length(min=8, max=15, message="비밀번호는 8자 이상, 15자 이하여야 합니다.")
        ],
        render_kw={"placeholder": ""}
    )
    submit = SubmitField(label="회원가입")