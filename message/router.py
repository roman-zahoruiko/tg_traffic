from typing import List
from fastapi import APIRouter, Depends
from database import User
from message.repository import MessageRepository
from message.schemas import MessageCreateSchema, MessageResponseSchema
from auth.dependencies import user_access, manager_user, admin_user

message_router = APIRouter(
    prefix='/messages',
    tags=['Messages'],
)


@message_router.post('/add')
async def add_message(msg: MessageCreateSchema, user: User = Depends(user_access)) -> MessageResponseSchema:
    message_obj = await MessageRepository.add_one(msg=msg, user=user)
    return MessageResponseSchema.from_orm(message_obj)


@message_router.get('/my')
async def get_user_messages(user: User = Depends(user_access)) -> List[MessageResponseSchema]:
    messages = await MessageRepository.get_user_messages(user=user)
    return [MessageResponseSchema.from_orm(message) for message in messages]


@message_router.get('/manager')
async def get_manager_messages(user: User = Depends(manager_user)) -> List[MessageResponseSchema]:
    messages = await MessageRepository.get_manager_messages(user=user)
    return [MessageResponseSchema.from_orm(message) for message in messages]


@message_router.get('/admin')
async def get_admin_messages(user: User = Depends(admin_user)) -> List[MessageResponseSchema]:
    messages = await MessageRepository.get_admin_messages()
    return [MessageResponseSchema.from_orm(message) for message in messages]
