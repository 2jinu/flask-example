from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER, DATETIME, LONGTEXT, VARCHAR

from my_app import db

class Comment(db.Model):
    __tablename__ = "comments"
    id = Column(
        INTEGER(display_width=11, unsigned=True),
        primary_key=True,
        autoincrement="auto",
        comment="댓글 식별 값"
    )
    content = Column(
        LONGTEXT(),
        nullable=False,
        comment="댓글 내용"
    )
    created = Column(
        DATETIME(),
        nullable=False,
        default=func.now(),
        comment="댓글 작성 일시"
    )
    username = Column(
        VARCHAR(length=50),
        ForeignKey(column="users.username", onupdate="CASCADE"),
        nullable=False
    )