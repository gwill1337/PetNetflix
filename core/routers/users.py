from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import (
    CreateUser,
    ResponseOut,
)

from db import (
    Users,
)
from main import get_db

router = APIRouter()

@router.post("/user")
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ResponseOut:
    stmt = Users(username=body.username, password_hash="pass")
    db.add(stmt)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Server Error {e}")
    return ResponseOut(message="User created")
