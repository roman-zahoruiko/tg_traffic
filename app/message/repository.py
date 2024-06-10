from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from database import async_session_maker, Message, User
from message.schemas import MessageCreateSchema
from message.telegram_handler import send_telegram_message


class MessageRepository:

    @classmethod
    async def add_one(cls, msg: MessageCreateSchema, user: 'User') -> Message:
        async with async_session_maker() as session:

            message_obj = Message(**msg.dict(), author_id=user.id)
            session.add(message_obj)

            tg_message_response = await send_telegram_message(
                bottoken=message_obj.bottoken,
                chatid=message_obj.chatid,
                message=message_obj.message
            )
            message_obj.response = tg_message_response

            await session.commit()
            await session.refresh(message_obj)

            return message_obj

    @classmethod
    async def get_user_messages(cls, user: 'User') -> List['Message']:
        async with async_session_maker() as session:
            result = await session.execute(select(Message).where(Message.author_id == user.id))
            return result.scalars().all()

    @classmethod
    async def get_manager_messages(cls, user: 'User') -> List['Message']:
        async with async_session_maker() as session:

            current_user = await session.get(User, user.id, options=[selectinload(User.managed_users)])
            managed_users_ids = [user.id for user in current_user.managed_users]
            query = select(Message).filter(Message.author_id.in_(managed_users_ids))

            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_admin_messages(cls) -> List['Message']:
        async with async_session_maker() as session:
            result = await session.execute(select(Message))
            return result.scalars().all()
