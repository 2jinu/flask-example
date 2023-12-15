from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, TextAreaField, SubmitField, SelectField
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

class SearchForm(FlaskForm):
    search_by = SelectField(
        choices=[
            ("title", "제목"),
            ("content", "내용"),
            ("user", "글쓴이")
        ],
        validators=[
            DataRequired(message="검색 타입을 입력하세요.")
        ]
    )
    search = StringField(
        validators=[
            Length(min=0, max=50, message="검색어는 50자 이하여야 합니다.")
        ]
    )
    submit = SubmitField(
        label="작성"
    )