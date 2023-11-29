from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length

class WriteForm(FlaskForm):
    title = StringField(
        label="제목",
        validators=[
            DataRequired(message="제목을 입력하세요."),
            Length(min=1, max=255, message="제목은 1자 이상, 255자 이하여야 합니다.")
        ]
    )
    content = TextAreaField(
        label="내용",
        validators=[
            DataRequired(message="내용을 입력하세요.")
        ]
    )
    attachments = MultipleFileField(
        label="첨부파일"
    )
    submit = SubmitField(
        label="작성"
    )