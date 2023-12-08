from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER, DATETIME, LONGTEXT, VARCHAR, BOOLEAN

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
    secret = Column(
        BOOLEAN(),
        nullable=False,
        default=False,
        comment="비밀 댓글"
    )
    username = Column(
        VARCHAR(length=50),
        ForeignKey(column="users.username", onupdate="CASCADE"),
        nullable=False
    )

    def __repr__(self):
        return f"Comment(id={self.id}, secret={self.secret}, username={self.username}, content={self.content})"