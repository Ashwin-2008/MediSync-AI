import uuid
from typing import List, Optional
from datetime import datetime
from pydantic import EmailStr, Field
from .base import BaseSchema, UUIDSchema, PaginationSchema

# Permission Schemas
class PermissionBase(BaseSchema):
    name: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None

class PermissionResponse(PermissionBase, UUIDSchema):
    pass

# Role Schemas
class RoleBase(BaseSchema):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None

class RoleResponse(RoleBase, UUIDSchema):
    pass

class RoleWithPermissionsResponse(RoleResponse):
    permissions: List[PermissionResponse] = []

# User Schemas
class UserBase(BaseSchema):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    role_id: uuid.UUID

class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    role_id: Optional[uuid.UUID] = None

class UserResponse(UserBase, UUIDSchema):
    role_id: uuid.UUID
    
class UserWithRoleResponse(UserResponse):
    role: Optional[RoleResponse] = None

class PaginatedUserResponse(PaginationSchema):
    items: List[UserResponse]

# API Key Schemas
class APIKeyBase(BaseSchema):
    name: str
    is_active: bool = True
    expires_at: Optional[datetime] = None

class APIKeyCreate(APIKeyBase):
    pass

class APIKeyResponse(APIKeyBase, UUIDSchema):
    key_prefix: str
    user_id: uuid.UUID

# Audit Log
class AuditLogResponse(UUIDSchema):
    user_id: Optional[uuid.UUID] = None
    action: str
    entity_type: str
    entity_id: str
    details: Optional[dict] = None
    ip_address: Optional[str] = None
