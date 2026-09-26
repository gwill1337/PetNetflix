from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from schemas import (
    AddFavorite,
    ResponseOut,
)

from db import (
    UsersFavorite
)

from main import get_db

router = APIRouter()

@router.post("/favorite/{user_id}")
async def add_to_favorite(user_id: int, body: AddFavorite, db: AsyncSession = Depends(get_db)) -> ResponseOut:
    stmt = UsersFavorite(user_id=user_id, movie_id=body.movie_id)
    db.add(stmt)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")
    return ResponseOut(message="Movie added to favorites")

@router.delete("/favorite/{user_id}")
async def delete_from_favorite(user_id: int, body: AddFavorite, db: AsyncSession = Depends(get_db)) -> ResponseOut:
    stmt = delete(UsersFavorite).where(UsersFavorite.user_id == user_id, UsersFavorite.movie_id == body.movie_id)
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")
    return ResponseOut(message="Movie deleted from favorites")

@router.get("/favorites_test")
async def get_favorites(
    db: AsyncSession = Depends(get_db),
):
    query = select(UsersFavorite)
    pre_res = await db.execute(query)
    res = pre_res.scalars().all()
    return res

@router.get("/favorites/{user_id}")
async def get_user_favorites(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    query = select(UsersFavorite.movie_id).where(UsersFavorite.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()
