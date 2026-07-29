import uuid
from typing import Optional, Any
from fastapi.encoders import jsonable_encoder
from backend.core.auth import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import CRUDBase
from backend.models.auth import User, Role, Permission, APIKey
from backend.schemas.auth import UserCreate, UserUpdate, RoleCreate, RoleUpdate, PermissionCreate, PermissionUpdate, APIKeyCreate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        password = obj_in_data.pop("password")
        obj_in_data["hashed_password"] = get_password_hash(password)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Role]:
        result = await db.execute(select(Role).filter(Role.name == name))
        return result.scalars().first()

class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    pass

class CRUDAPIKey(CRUDBase[APIKey, APIKeyCreate, APIKeyCreate]): # Update doesn't strictly have a schema
    async def get_by_prefix(self, db: AsyncSession, *, prefix: str) -> Optional[APIKey]:
        result = await db.execute(select(APIKey).filter(APIKey.key_prefix == prefix))
        return result.scalars().first()

user = CRUDUser(User)
role = CRUDRole(Role)
permission = CRUDPermission(Permission)
api_key = CRUDAPIKey(APIKey)
