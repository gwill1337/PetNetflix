import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from config import settings

def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def check_password(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

async def create_jwt(d: dict, exp_int: int):
    res_dict: dict = d.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(seconds=exp_int)
    res_dict.update({"exp": expire_time})
    res = jwt.encode(res_dict, settings.jwt_key, algorithm=settings.jwt_algorithm)
    return res

async def check_jwt(token: str):
    return jwt.decode(token, settings.jwt_key, algorithms=[settings.jwt_algorithm])
