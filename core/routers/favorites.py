from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from .auth import get_current_user
from schemas import (
    AddFavorite,
    ResponseOut,
)

from db import (
    UsersFavorite,
    get_db,
)

router = APIRouter()

@router.post("/favorite")
async def add_to_favorite(
    body: AddFavorite,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ResponseOut:
    stmt = UsersFavorite(user_id=user_id, movie_id=body.movie_id)
    db.add(stmt)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")
    return ResponseOut(message="Movie added to favorites")

@router.delete("/favorite")
async def delete_from_favorite(
    body: AddFavorite,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ResponseOut:
    stmt = delete(UsersFavorite).where(UsersFavorite.user_id == user_id, UsersFavorite.movie_id == body.movie_id)
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")
    return ResponseOut(message="Movie deleted from favorites")

@router.get("/favorites")
async def get_user_favorites(
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(UsersFavorite.movie_id).where(UsersFavorite.user_id == user_id)
    res = await db.execute(query)
    return res.scalars().all()
