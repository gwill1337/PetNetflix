from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

from starlette.middleware.sessions import SessionMiddleware
from db import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors,
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
    oauth,
)

app.include_router(auth.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(favorites.router, prefix="/api")
app.include_router(movies.router, prefix="/api")
app.include_router(movies.admin_router, prefix="/api")
app.include_router(oauth.router, prefix="/api")