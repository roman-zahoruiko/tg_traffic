from fastapi import APIRouter, Depends, HTTPException, status
from auth.backend import fastapi_users, auth_backend
from auth.dependencies import admin_user
from auth.repository import UserRepository
from auth.schemas import UserReadSchema, UserCreateSchema, RoleUpdateSchema, ManagerUserAssignmentSchema
from database import User

auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

auth_router.include_router(
    fastapi_users.get_register_router(UserReadSchema, UserCreateSchema),
    prefix="/auth",
    tags=["Auth"],
)


admin_router = APIRouter(
    prefix='/admin',
    tags=['Admin'],
)


@admin_router.put("/users/role")
async def update_user_role(role_update: RoleUpdateSchema, current_user: User = Depends(admin_user)) -> UserReadSchema:

    updated_user = await UserRepository.update_user_role(role_update=role_update)

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserReadSchema.from_orm(updated_user)


@admin_router.post('/users/assign_user')
async def assign_users_to_manager(
    assignment: ManagerUserAssignmentSchema,
    current_user: User = Depends(admin_user),
) -> ManagerUserAssignmentSchema:

    if assignment.user_id == assignment.manager_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Manager can not assign himself')

    assignment = await UserRepository.assign_user_to_manager(assignment=assignment)

    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User or Manager not found')

    return ManagerUserAssignmentSchema.from_orm(assignment)
