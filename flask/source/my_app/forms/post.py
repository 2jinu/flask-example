from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class WriteForm(FlaskForm):
    title = StringField(
        label="제목",
        validators=[
            DataRequired(message="제목을 입력하세요."),
            Length(min=1, max=255, message="제목은 1자 이상, 255자 이하여야 합니다.")
        ],
        render_kw={"autofocus": True}
    )
    content = TextAreaField(
        label="내용"
    )
    attachments = MultipleFileField(
        label="첨부파일"
    )
    submit = SubmitField(
        label="작성"
    )

class CommentForm(FlaskForm):
    content = TextAreaField(
        label="내용",
        validators=[
            DataRequired(message="댓글을 입력하세요.")
        ]
    )
    submit = SubmitField(
        label="작성"
    )