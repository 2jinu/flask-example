from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TEXT, DATETIME
from werkzeug.utils import secure_filename
from hashlib import sha3_256
from datetime import datetime

from my_app import db

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
    view_count = Column(
        INTEGER(display_width=11, unsigned=True),
        nullable=False,
        default=0,
        comment="게시글 조회수"
    )
    user = relationship(
        argument="User",
        secondary="user_posts",
        backref=backref(name="posts", lazy="dynamic"),
        uselist=False
    )
    files = relationship(
        argument="File",
        secondary="post_files",
        backref=backref(name="posts", lazy="dynamic"),
        uselist=True
    )
    views = relationship(
        argument="PostViews",
        backref=backref(name="posts"),
        uselist=True
    )

    def __init__(self, title:str, content:str, user, files):
        self.title = title
        self.content = content
        self.user = user
        self.files = files

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, created={self.created}, user={self.user}, files={self.files}, views={self.views})"
    
class File(db.Model):
    __tablename__ = "files"
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="파일 식별 값"
    )
    original_name = Column(
        VARCHAR(length=255),
        nullable=False,
        comment="원본 파일 이름"
    )
    stored_name = Column(
        VARCHAR(length=255),
        nullable=False,
        comment="저장 파일 이름"
    )

    def __init__(self, original_name:str):
        self.original_name = secure_filename(filename=original_name)
        self.stored_name = sha3_256(f"{datetime.now()}{self.original_name}".encode()).hexdigest()
    
    def __repr__(self) -> str:
        return f"File(id={self.id}, original_name={self.original_name}, stored_name={self.stored_name})"

class UserPosts(db.Model):
    __tablename__ = "user_posts"
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="사용자 게시글 매핑 식별 값"
    )
    user_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="users.id", ondelete="CASCADE"),
        nullable=False,
        comment="사용자 식별 값"
    )
    post_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="posts.id", ondelete="CASCADE"),
        nullable=False,
        comment="게시글 식별 값"
    )

class PostFiles(db.Model):
    __tablename__ = "post_files"
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="게시글 첨부파일 매핑 식별 값"
    )
    post_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="posts.id", ondelete="CASCADE"),
        nullable=False,
        comment="게시글 식별 값"
    )
    file_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="files.id", ondelete="CASCADE"),
        nullable=False,
        comment="첨부파일 식별 값"
    )

class PostViews(db.Model):
    __tablename__ = "post_views"
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="게시글 조회 매핑 식별 값"
    )
    post_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="posts.id", ondelete="CASCADE"),
        nullable=False,
        comment="게시글 식별 값"
    )
    user_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="users.id"),
        nullable=False,
        comment="사용자 식별 값"
    )