from fastapi import Depends, HTTPException, status
from auth.backend import fastapi_users
from database import User, UserRole

current_active_user = fastapi_users.current_user(active=True)


async def admin_user(current_user: User = Depends(current_active_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Admins only"
        )
    return current_user


async def manager_user(current_user: User = Depends(current_active_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Managers only"
        )
    return current_user


async def user_access(current_user: User = Depends(current_active_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER, UserRole.USER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Users only"
        )
    return current_user
