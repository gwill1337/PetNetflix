from contextlib import asynccontextmanager
from typing import List
import bcrypt
import jwt
from uuid import uuid4
from hashlib import sha256
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, Query, status, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey, Text, exists, select, delete, func
from config import settings

from schemas import (
    NewMovie,
    EditMovie,
    AddFavorite,
    CreateUser,
    LoginUser,
    UserOut,
    NewComment,
    CommentOut,
)
from starlette.middleware.sessions import SessionMiddleware
from db import engine, SessionLocal

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

app.add_middleware(SessionMiddleware, secret_key=settings.jwt_key)


@app.get("/get")
async def get_something():
    return {"Message": "Hello"}


from routers import ( # noqa: F401 E402
    auth,
    comments,
    favorites,
    movies,
    users,
    oauth,
)

app.include_router(auth.router)
app.include_router(comments.router)
app.include_router(favorites.router)
app.include_router(movies.router)
app.include_router(users.router)
app.include_router(oauth.router)