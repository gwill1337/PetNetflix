from contextlib import asynccontextmanager
import bcrypt
import jwt
from uuid import uuid4
from hashlib import sha256
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, Query, status, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, Text, exists, select, delete
from config import settings

from schemes import (
    NewMovie,
    EditMovie,
    AddFavorite,
    CreateUser,
    LoginUser,
    UserOut,
)

engine = create_async_engine(settings.database_url)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

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
    password_hash: Mapped[str]

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
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

async def get_db():
    async with SessionLocal() as db:
        yield db

# app = FastAPI(lifespan=lifespan)
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

@app.get("/movie/{movie_id}")
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await db.get(Movies, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")
    return movie

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
    stmt = Movies(name=body.name, image=body.image, rating=body.rating, year=body.year, title=body.title, description=body.description)
    db.add(stmt)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")
    return {"Message": "Movie added to database"}

@app.put("/movie/{movie_id}")
async def edit_movie(movie_id: int, body: EditMovie, db: AsyncSession = Depends(get_db)):
    movie = await db.get(Movies, movie_id)

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found.")

    movie.name = body.name
    movie.title = body.title
    movie.description = body.description
    movie.image = body.image
    movie.rating = body.rating
    movie.year = body.year

    try:
        await db.commit()
        await db.refresh(movie)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

    return {"Message": "Movie updated successfully"}

@app.post("/favorite/{user_id}")
async def add_to_favorite(user_id: int, body: AddFavorite, db: AsyncSession = Depends(get_db)):
    stmt = UsersFavorite(user_id=user_id, movie_id=body.movie_id)
    db.add(stmt)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")
    return {"Message": "Movie added to favorites"}

@app.delete("/favorite/{user_id}")
async def delete_from_favorite(user_id: int, body: AddFavorite, db: AsyncSession = Depends(get_db)):
    stmt = delete(UsersFavorite).where(UsersFavorite.user_id == user_id, UsersFavorite.movie_id == body.movie_id)
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

@app.get("/favorites/{user_id}")
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


def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def check_password(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

async def create_jwt(d: dict, exp_int: int):
    res_dict: dict = d.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(seconds=exp_int)
    res_dict.update({"exp": expire_time})
    res = jwt.encode(res_dict, settings.jwt_key, algorithm=settings.jwt_algorithm)
    return res

async def check_jwt(token: str):
    return jwt.decode(token, settings.jwt_key, algorithms=[settings.jwt_algorithm])

@app.post("/auth/login")
async def login(
    body: LoginUser,
    resp: Response,
    db: AsyncSession = Depends(get_db),
):

    query = select(Users).where(Users.email == body.email)
    pre_res = await db.execute(query)
    user = pre_res.scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not exists.")

    if not check_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

    payload = {"sub": str(user.user_id)}
    token = await create_jwt(payload, 60*60*12)
    new_uuid = str(uuid4())
    refresh_payload = {"sub": user.user_id, "session_id": new_uuid}
    refresh_token = await create_jwt(refresh_payload, 60*60*24*7)
    hashed_refresh_token = sha256(refresh_token.encode("utf-8")).hexdigest()

    new_session = UserSessions(user_id=user.user_id, session_uuid=new_uuid, refresh_token_hash=hashed_refresh_token)
    db.add(new_session)
    try:
        await db.commit()
        await db.refresh(new_session)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error to add new session to db. {e}")

    resp.set_cookie("token", token, samesite="lax", httponly=True)
    resp.set_cookie("refresh_token", refresh_token, samesite="lax", httponly=True)
    return {"Message": "Loged in successfully"}
    

async def get_current_user(token: str = Cookie(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Not auth")
    try:
        res = await check_jwt(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(res["sub"])

@app.get("/me", response_model=UserOut)
async def get_detail_user(
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Users).where(Users.user_id == user_id)
    try:
        res = await db.execute(query)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return res.scalars().first()

@app.post("/auth/register")
async def register(
    body: CreateUser,
    resp: Response,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(exists().where(Users.email == body.email))
    user_exists = await db.scalar(stmt)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Already exists.")
    hashed_password = hash_password(body.password)
    stmt = Users(username=body.username, email=body.email,password_hash=hashed_password)
    db.add(stmt)
    try:
        await db.commit()
        await db.refresh(stmt)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"server error {e}")
    login_data = LoginUser(
        username=body.username,
        email=body.email,
        password=body.password,
    )
    await login(body=login_data,resp=resp , db=db)
    return {"Message": "User created successfully"}

@app.get("/users")
async def get_users_test(db: AsyncSession = Depends(get_db)):
    q = select(Users)
    res = await db.execute(q)
    return res.scalars().all()

@app.post("/auth/refresh")
async def refresh_token(
    resp: Response,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
):  
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token found")

    try:
        user_token = await check_jwt(refresh_token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    if user_token:
        token_session = user_token.get("session_id")
        token_hash = sha256(refresh_token.encode("utf-8")).hexdigest()
        sub_raw = user_token.get("sub")
        if not sub_raw:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        user_id = int(sub_raw)
        query = select(UserSessions).where(UserSessions.user_id == user_id, UserSessions.refresh_token_hash == token_hash, UserSessions.session_uuid == token_session)
        try:
            res = await db.execute(query)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
        session = res.scalars().one_or_none()

        if session:

            new_token = await create_jwt({"sub": session.user_id}, 60*60*12)
            new_uuid = str(uuid4())
            refresh_payload = {"sub": str(session.user_id), "session_id": new_uuid}
            new_refresh_token = await create_jwt(refresh_payload, 60*60*24*7)
            new_refresh_token_hash = sha256(new_refresh_token.encode("utf-8")).hexdigest()
            
            resp.set_cookie("token", new_token, samesite="lax", httponly=True)
            resp.set_cookie("refresh_token", new_refresh_token, samesite="lax", httponly=True)
            
            session.refresh_token_hash = new_refresh_token_hash
            try:
                await db.commit()
                await db.refresh(session)
            except Exception as e:
                await db.rollback()
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

            return {"Message": "Refresh ended successfully"}

@app.post("/auth/logout")
async def logout(
    resp: Response,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
):
    if not refresh_token:

        resp.delete_cookie("token")
        resp.delete_cookie("refresh_token")
        return {"Message": "Logged out successfully"}

    try:
        user_token = await check_jwt(refresh_token)
    except Exception as e:

        resp.delete_cookie("token")
        resp.delete_cookie("refresh_token")
        return {"Message": "Logged out successfully", "note": f"token was already invalid: {e}"}

    token_session = user_token.get("session_id")
    token_hash = sha256(refresh_token.encode("utf-8")).hexdigest()
    sub_raw = user_token.get("sub")

    if sub_raw:
        user_id = int(sub_raw)
        stmt = delete(UserSessions).where(
            UserSessions.user_id == user_id,
            UserSessions.refresh_token_hash == token_hash,
            UserSessions.session_uuid == token_session,
        )
        try:
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            await db.rollback()
            resp.delete_cookie("token")
            resp.delete_cookie("refresh_token")
            return {"Message": "Logged out successfully", "note": f"session cleanup failed: {e}"}

    resp.delete_cookie("token")
    resp.delete_cookie("refresh_token")
    return {"Message": "Logged out successfully"}