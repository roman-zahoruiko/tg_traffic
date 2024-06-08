from fastapi_users import schemas
from pydantic import BaseModel
from database import UserRole


class UserReadSchema(schemas.BaseUser[int]):
    full_name: str
    role: UserRole


class UserCreateSchema(schemas.BaseUserCreate):
    full_name: str


class RoleUpdateSchema(BaseModel):
    user_id: int
    new_role: UserRole


class ManagerUserAssignmentSchema(BaseModel):
    manager_id: int
    user_id: int

    class Config:
        from_attributes = True
