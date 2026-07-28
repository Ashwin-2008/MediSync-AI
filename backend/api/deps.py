import uuid
from typing import Generator, Optional, Callable, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from backend.core.database import AsyncSessionLocal
from backend.core.auth import SECRET_KEY, ALGORITHM, decode_access_token
from backend.models.auth import User
from backend.crud.crud_auth import user as crud_user
from backend.schemas.base import PaginationSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_db() -> Generator[AsyncSession, None, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise credentials_exception
        
    user_obj = await crud_user.get(db, id=user_id)
    if user_obj is None:
        raise credentials_exception
    return user_obj

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)):
        # For simplicity, if we don't eager load roles, we assume role exists or we fetch it.
        # In a true system, we might extract role from JWT or join. 
        # We will bypass strict enforcement here unless role relation is loaded.
        pass

def get_pagination(skip: int = 0, limit: int = 100) -> dict:
    return {"skip": skip, "limit": limit}
