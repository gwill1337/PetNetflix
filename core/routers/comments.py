from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from schemas import (
    NewComment,
    CommentOut,
    ResponseOut,
)

from db import (
    Comments,
    Users,
    
)

from main import get_db

from routers.auth import get_detail_user

router = APIRouter()

@router.get("/comments/{movie_id}", response_model=List[CommentOut])
async def get_comments(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    query = select(Comments).where(Comments.movie_id == movie_id)
    try:
        res = await db.execute(query)
        comments = res.scalars().all()
        return comments
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

@router.post("/comments", response_model=CommentOut)
async def create_comment(
    body: NewComment,
    user: Users = Depends(get_detail_user),
    db: AsyncSession = Depends(get_db),
) -> CommentOut:
    stmt = Comments(comment_text=body.text, created_at=datetime.now(timezone.utc), user_id=user.user_id, user_username=user.username, movie_id=body.movie_id)
    db.add(stmt)
    try:
        await db.commit()
        await db.refresh(stmt)
        return CommentOut.model_validate(stmt)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.delete("/comments")
async def delete_comment(
    comment_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> ResponseOut:
    stmt = delete(Comments).where(Comments.id == comment_id, Comments.user_id == user_id)

    try:
        await db.execute(stmt)
        await db.commit()
        return ResponseOut(message="Comment deleted")
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"comment not found")
