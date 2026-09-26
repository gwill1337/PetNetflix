import jwt
from uuid import uuid4
from hashlib import sha256
from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select, delete

from schemas import (
    CreateUser,
    LoginUser,
    UserOut,
    ResponseOut,
)

from db import (
    Users,
    UserSessions,
    get_db,
)

from security import (
    hash_password,
    check_password,
    create_jwt,
    check_jwt,
)

router = APIRouter()

@router.post("/auth/login")
async def login(
    body: LoginUser,
    resp: Response,
    db: AsyncSession = Depends(get_db),
) -> ResponseOut:

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
    return ResponseOut(message="Loged in successfully")

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

@router.get("/me", response_model=UserOut)
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

async def get_current_admin(
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(Users, user_id)
    if not user or not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user_id

@router.post("/auth/register")
async def register(
    body: CreateUser,
    resp: Response,
    db: AsyncSession = Depends(get_db),
) -> ResponseOut:
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
    return ResponseOut(message="User created successfully")

@router.post("/auth/refresh")
async def refresh_token(
    resp: Response,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
) -> ResponseOut:
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token found")

    try:
        user_token = await check_jwt(refresh_token)
    except Exception:
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
        except Exception:
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

            return ResponseOut(message="Refresh ended successfully")
    return ResponseOut(message="Unexpected error")

@router.post("/auth/logout")
async def logout(
    resp: Response,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
) -> ResponseOut:
    if not refresh_token:

        resp.delete_cookie("token")
        resp.delete_cookie("refresh_token")
        return ResponseOut(message="Logged out successfully")

    try:
        user_token = await check_jwt(refresh_token)
    except Exception as e:

        resp.delete_cookie("token")
        resp.delete_cookie("refresh_token")
        return ResponseOut(message="Logged out successfully")

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
            return ResponseOut(message="Logged out successfully")

    resp.delete_cookie("token")
    resp.delete_cookie("refresh_token")
    return ResponseOut(message="Logged out successfully")
