from hashlib import sha256
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request, Depends, status
from authlib.integrations.starlette_client import OAuth
from sqlalchemy import select
from fastapi.responses import RedirectResponse
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from db import UserSessions, Users
from security import create_jwt
from main import get_db


router = APIRouter()

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/auth/google/login")
async def google_login(request: Request):
    redirect_uri = settings.google_redirect_uri
    print("DEBUG redirect_uri:", repr(redirect_uri))
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        return RedirectResponse(f"{settings.frontend_url}?auth_error=1")

    userinfo = token.get("userinfo")
    if not userinfo or not userinfo.get("email_verified"):
        return RedirectResponse(f"{settings.frontend_url}?auth_error=1")

    sub = userinfo["sub"]
    email = userinfo["email"]

    query = select(Users).where(Users.oauth_sub == sub)
    res = await db.execute(query)
    user = res.scalars().one_or_none()

    if not user:
        query = select(Users).where(Users.email == email)
        res = await db.execute(query)
        user = res.scalars().one_or_none()

        if not user:
            username = userinfo.get("name") or email.split("@")[0]
            user = Users(
                username=username,
                email=email,
                password_hash=None,
                oauth_provider="google",
                oauth_sub=sub,
            )
            db.add(user)
        else:
            user.oauth_provider = "google"
            user.oauth_sub = sub

        try:
            await db.commit()
            await db.refresh(user)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Server error: {e}")

    resp = RedirectResponse(settings.frontend_url)

    payload = {"sub": str(user.user_id)}
    access_token = await create_jwt(payload, 60*60*12)
    new_uuid = str(uuid4())
    refresh_payload = {"sub": user.user_id, "session_id": new_uuid}
    refresh_token = await create_jwt(refresh_payload, 60*60*24*7)
    hashed_refresh_token = sha256(refresh_token.encode("utf-8")).hexdigest()

    new_session = UserSessions(user_id=user.user_id, session_uuid=new_uuid, refresh_token_hash=hashed_refresh_token)
    db.add(new_session)
    await db.commit()

    resp.set_cookie("token", access_token, samesite="lax", httponly=True)
    resp.set_cookie("refresh_token", refresh_token, samesite="lax", httponly=True)
    return resp