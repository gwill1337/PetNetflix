from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select

from schemas import (
    CreateUser,
    ResponseOut,
)

from db import (
    Users,
    
)
from main import get_db

router = APIRouter()



@router.get("/users")
async def get_users_test(db: AsyncSession = Depends(get_db)):
    q = select(Users)
    res = await db.execute(q)
    return res.scalars().all()

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