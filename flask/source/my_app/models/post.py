from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, LONGTEXT, CHAR
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.utils import secure_filename
from hashlib import sha3_256, sha256
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
        LONGTEXT(),
        nullable=False,
        comment="게시글 내용"
    )
    username = Column(
        VARCHAR(length=50),
        ForeignKey(column="users.username", onupdate="CASCADE"),
        nullable=False,
        comment="게시글 글쓴이"
    )
    created = Column(
        DATETIME(),
        nullable=False,
        default=func.now(),
        comment="게시글 작성 일시"
    )
    views = Column(
        INTEGER(display_width=11, unsigned=True),
        nullable=False,
        default=0,
        comment="게시글 조회수"
    )
    files = relationship(
        argument="File",
        secondary="rel_post_files",
        backref=backref(name="posts", lazy="dynamic"),
        uselist=True
    )
    comments = relationship(
        argument="Comment",
        secondary="rel_post_comments",
        backref=backref(name="posts"),
        uselist=True
    )

    def __init__(self, title:str, content:str, username:str, files:list):
        self.title = title
        self.content = content
        self.username = username
        self.files = files

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, created={self.created}, username={self.username}, files={self.files}, views={self.views})"
    
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
    size = Column(
        INTEGER(display_width=11, unsigned=True),
        nullable=False,
        comment="파일 크기 (Byte)"
    )
    hash = Column(
        CHAR(length=128),
        nullable=False,
        comment="파일 해시(SHA-256)"
    )

    def __init__(self, file:FileStorage):
        self.original_name = secure_filename(filename=file.filename)
        self.stored_name = sha3_256(f"{datetime.now()}{self.original_name}".encode()).hexdigest()
        file_data = file.read()
        file.seek(0)
        self.size = int(len(file_data))
        self.hash = sha256(string=file_data).hexdigest()
    
    def __repr__(self) -> str:
        return f"File(id={self.id}, original_name={self.original_name}, stored_name={self.stored_name}, size={self.size}, hash={self.hash})"

class PostFiles(db.Model):
    __tablename__ = "rel_post_files"
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

class PostComments(db.Model):
    __tablename__ = "rel_post_comments"
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="사용자 댓글 매핑 식별 값"
    )
    post_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="posts.id", ondelete="CASCADE"),
        nullable=False,
        comment="게시글 식별 값"
    )
    comment_id = Column(
        INTEGER(display_width=11, unsigned=True),
        ForeignKey(column="comments.id", ondelete="CASCADE"),
        nullable=False,
        comment="댓글 식별 값"
    )