from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TEXT, DATETIME

from my_app import db

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
    submit = SubmitField(
        label="작성"
    )

class Post(db.Model):
    __tablename__ = "posts"
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="게시글 식별 값"
    )
    title = Column(
        VARCHAR(length=255),
        nullable=False,
        comment="게시글 제목"
    )
    content = Column(
        TEXT(),
        nullable=False,
        comment="게시글 내용"
    )
    created = Column(
        DATETIME(),
        nullable=False,
        default=func.now(),
        comment="게시글 작성 일시"
    )
    user = relationship(
        argument="User",
        secondary="user_posts",
        backref=backref(name="posts", lazy="dynamic"),
        uselist=False
    )

    def __init__(self, title:str, content:str, user:list):
        self.title = title
        self.content = content
        self.user = user

    def __repr__(self):
        return f"Post(id='{self.id}', title='{self.title}', created={self.created}, user={self.user})"
    
class UserPosts(db.Model):
    __tablename__ = 'user_posts'
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="사용자 게시글 매핑 식별 값"
    )
    user_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="users.id", ondelete="CASCADE"),
        comment="사용자 식별 값"
    )
    post_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="posts.id", ondelete="CASCADE"),
        comment="게시글 식별 값"
    )