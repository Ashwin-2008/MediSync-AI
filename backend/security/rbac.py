from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from .auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class RBAC:
    """Role-Based Access Control decorator/dependency."""
    
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, token: str = Security(oauth2_scheme)):
        payload = verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        user_role = payload.get("role")
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this role"
            )
        return payload
