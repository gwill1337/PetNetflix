from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas import (
    NewMovie,
    EditMovie,
    ResponseOut,
)
from db import (
    Movies,
)
from main import get_db

from .auth import get_current_admin

router = APIRouter(
    tags=["user"]
)

admin_router = APIRouter(
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)

@router.get("/movies")
async def get_movies(
    db: AsyncSession = Depends(get_db),
):
    query = select(Movies)
    pre_res = await db.execute(query)
    res = pre_res.scalars().all()
    return res

@router.get("/movie/{movie_id}")
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await db.get(Movies, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")
    return movie

@router.get("/search/movie")
async def search_for_movie(
    movie_name: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(Movies).where(Movies.name.ilike(f"%{movie_name.strip()}%")).offset(offset).limit(limit)

    res = await db.execute(query)
    return res.scalars().all()

@admin_router.post("/movie")
async def add_movie(body: NewMovie, db: AsyncSession = Depends(get_db)) -> ResponseOut:
    stmt = Movies(name=body.name, image=body.image, rating=body.rating, year=body.year, title=body.title, description=body.description)
    db.add(stmt)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")
    return ResponseOut(message="Movie added to database")

@admin_router.put("/movie/{movie_id}")
async def edit_movie(movie_id: int, body: EditMovie, db: AsyncSession = Depends(get_db)) -> ResponseOut:
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

    return ResponseOut(message="Movie updated successfully")
