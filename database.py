from enum import Enum
from datetime import datetime
from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, BigInteger, String, ForeignKey, Boolean, Text
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class ManagerUserAssociation(Base):
    __tablename__ = 'manager_user_association'

    manager_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(length=256), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLAlchemyEnum(UserRole), default=UserRole.USER, nullable=False)

    managed_users: Mapped[list['User']] = relationship(
        'User',
        secondary='manager_user_association',
        primaryjoin=id == ManagerUserAssociation.manager_id,
        secondaryjoin=id == ManagerUserAssociation.user_id,
        backref='managers'
    )
    messages: Mapped[list['Message']] = relationship('Message', back_populates='author')


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    bottoken: Mapped[str] = mapped_column(String, nullable=False)
    chatid: Mapped[int] = mapped_column(BigInteger, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    author: Mapped[User] = relationship('User', back_populates="messages")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
