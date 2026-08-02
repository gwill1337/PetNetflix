from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, select, delete
from pydantic import BaseModel
from config import settings

engine = create_async_engine(settings.database_url)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class NewMovie(BaseModel):
    name: str
    image: str
    rating: float
    year: str

class AddFavorite(BaseModel):
    movie_id: int
    user_id: int

class CreateUser(BaseModel):
    username: str

class Base(DeclarativeBase):
    pass


class Movies(Base):
    __tablename__ = "movies"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    image: Mapped[str]
    rating: Mapped[float]
    year: Mapped[str]


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]

class UsersFavorite(Base):
    __tablename__ = "usersfavorite"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.movie_id", ondelete="CASCADE"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

async def get_db():
    async with SessionLocal() as db:
        yield db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)

@app.get("/get")
async def get_something():
    return {"Message": "Hello"}

@app.get("/movies")
async def get_movies(
    db: AsyncSession = Depends(get_db),
):
    query = select(Movies)
    pre_res = await db.execute(query)
    res = pre_res.scalars().all()
    return res

@app.get("/search/movie")
async def search_for_movie(
    movie_name: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(Movies).where(Movies.name.ilike(f"%{movie_name.strip()}%")).offset(offset).limit(limit)

    res = await db.execute(query)
    return res.scalars().all()

@app.post("/movie")
async def add_movie(body: NewMovie, db: AsyncSession = Depends(get_db)):
    stmt = Movies(name=body.name, image=body.image, rating=body.rating, year=body.year)
    db.add(stmt)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")
    return {"Message": "Movie added to database"}

@app.post("/favorite")
async def add_to_favorite(body: AddFavorite, db: AsyncSession = Depends(get_db)):
    stmt = UsersFavorite(user_id=body.user_id, movie_id=body.movie_id)
    db.add(stmt)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")
    return {"Message": "Movie added to favorites"}

@app.delete("/favorite")
async def delete_from_favorite(body: AddFavorite, db: AsyncSession = Depends(get_db)):
    stmt = delete(UsersFavorite).where(UsersFavorite.user_id == body.user_id, UsersFavorite.movie_id == body.movie_id)
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")
    return {"Message": "Movie deleted from favorites"}

@app.get("/favorites_test")
async def get_favorites(
    db: AsyncSession = Depends(get_db),
):
    query = select(UsersFavorite)
    pre_res = await db.execute(query)
    res = pre_res.scalars().all()
    return res

@app.get("/favorites")
async def get_user_favorites(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    query = select(UsersFavorite.movie_id).where(UsersFavorite.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()

@app.post("/user")
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)):
    stmt = Users(username=body.username, password_hash="pass")
    db.add(stmt)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error {e}")
    return {"Message": "User created"}