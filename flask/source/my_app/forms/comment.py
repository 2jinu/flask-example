from flask_wtf import FlaskForm
from wtforms import TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    content = TextAreaField(
        label="내용",
        validators=[
            DataRequired(message="댓글을 입력하세요.")
        ]
    )
    secret = BooleanField(
        label="비밀 댓글"
    )
    submit = SubmitField(
        label="작성"
    )