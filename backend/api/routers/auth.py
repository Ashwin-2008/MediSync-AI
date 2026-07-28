import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api import deps
from backend.core.auth import verify_password, get_password_hash, create_access_token
from backend.schemas.auth import UserResponse, UserCreate
from backend.crud.crud_auth import user as crud_user
from backend.models.auth import User

router = APIRouter()

@router.post("/login", response_model=dict)
async def login_access_token(
    db: AsyncSession = Depends(deps.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests"""
    user = await crud_user.get_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
async def register(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """Create new user without the need to be logged in."""
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_in_dict = user_in.model_dump()
    user_in_dict["hashed_password"] = get_password_hash(user_in_dict.pop("password"))
    user = await crud_user.create(db, obj_in=user_in_dict)
    return user

@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get current user."""
    return current_user
