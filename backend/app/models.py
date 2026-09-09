from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


# =========================================================
# USER
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    comments = relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    votes = relationship(
        "Vote",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# =========================================================
# POST
# =========================================================

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(200),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    author = relationship(
        "User",
        back_populates="posts"
    )

    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    votes = relationship(
        "Vote",
        back_populates="post",
        cascade="all, delete-orphan"
    )


# =========================================================
# COMMENT
# =========================================================

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(
        Text,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    author = relationship(
        "User",
        back_populates="comments"
    )

    post = relationship(
        "Post",
        back_populates="comments"
    )


# =========================================================
# VOTE
# =========================================================

class Vote(Base):
    __tablename__ = "votes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    value = Column(
        Integer,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="votes"
    )

    post = relationship(
        "Post",
        back_populates="votes"
    )

    # One user can vote only once on a particular post
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "post_id",
            name="unique_user_post_vote"
        ),
    )