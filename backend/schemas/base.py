from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UUIDSchema(BaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class PaginationSchema(BaseSchema):
    total: int
    page: int
    size: int
    pages: int
