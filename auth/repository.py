from sqlalchemy import select, or_
from typing import Optional
from database import async_session_maker, User, ManagerUserAssociation, UserRole
from auth.schemas import RoleUpdateSchema, ManagerUserAssignmentSchema


class UserRepository:

    @classmethod
    async def update_user_role(cls, role_update: RoleUpdateSchema) -> Optional[User]:
        async with async_session_maker() as session:

            result = await session.execute(select(User).filter(User.id == role_update.user_id))
            user = result.scalars().first()

            if not user:
                return None

            user.role = role_update.new_role
            await session.commit()
            await session.refresh(user)

            return user

    @classmethod
    async def assign_user_to_manager(cls, assignment: ManagerUserAssignmentSchema) -> Optional[ManagerUserAssociation]:
        async with async_session_maker() as session:

            manager_query = select(User).filter(
                (User.id == assignment.manager_id) & or_(User.role == UserRole.MANAGER, User.role == UserRole.ADMIN)
            )
            manager_result = await session.execute(manager_query)
            manager = manager_result.scalars().first()

            user_result = await session.execute(select(User).filter(User.id == assignment.user_id))
            user = user_result.scalars().first()

            if not manager or not user:
                return None

            existing_association = await session.execute(
                select(ManagerUserAssociation)
                .filter(
                    (ManagerUserAssociation.manager_id == assignment.manager_id) &
                    (ManagerUserAssociation.user_id == assignment.user_id)
                )
            )
            existing_association_result = existing_association.scalar_one_or_none()
            if existing_association_result:
                return existing_association_result

            new_association = ManagerUserAssociation(manager_id=assignment.manager_id, user_id=user.id)
            session.add(new_association)
            await session.commit()

            return new_association
