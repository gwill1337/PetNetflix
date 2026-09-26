from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey, Text, func
from config import settings


engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=5,
    )
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as db:
        yield db

class Base(DeclarativeBase):
    pass

class Movies(Base):
    __tablename__ = "movies"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(Text)
    image: Mapped[str]
    rating: Mapped[float]
    year: Mapped[str]


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=True)
    oauth_provider: Mapped[str] = mapped_column(nullable=True)
    oauth_sub: Mapped[str] = mapped_column(nullable=True, unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

class UsersFavorite(Base):
    __tablename__ = "usersfavorite"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.movie_id", ondelete="CASCADE"))

class UserSessions(Base):
    __tablename__ = "usersessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    session_uuid: Mapped[str] = mapped_column(unique=True)
    refresh_token_hash: Mapped[str]

class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    user_username: Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.movie_id", ondelete="CASCADE"))
