from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from service_bot.database import User, Newsletter, connection

scheduler = AsyncIOScheduler()  # Инициализация планировщика
router = Router()


async def send_newsletter(user_id: int, message: str):
    await bot.send_message(user_id, message)


async def schedule_newsletter(user_id: int, message: str, send_at: datetime):
    scheduler.add_job(
        send_newsletter, DateTrigger(run_date=send_at), args=[user_id, message]
    )


@router.message(F.text & ~F.text.startswith("/"))
async def echo(message: Message):
    await message.reply(
        text="Спасибо за ваш выбор! Мы свяжемся с вами в ближайшее время"
    )


@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Привет! Я ваш автотвечик. Чем могу помочь?")


@router.message(Command("help"))
async def send_help(message: Message):
    await message.reply(
        "Я могу ответить на ваши вопросы и помочь с услугами. Напишите мне, и я постараюсь вам помочь!"
    )


@router.message(Command("subscribe"))
@connection
async def subscribe(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    username = message.from_user.username
    user_exists = await session.execute(select(User).filter_by(user_id=user_id))
    if not user_exists.scalar():
        # Если пользователь не существует, добавляем его
        await User.add_user(user_id=user_id, username=username, session=session)
    time_to_send = datetime.now() + timedelta(seconds=5)
    message_content = "Добро пожаловать в нашу рассылку!"
    await Newsletter.add_newsletter(
        user_id=user_id, message=message_content, send_at=time_to_send, session=session
    )
    await session.commit()
    await schedule_newsletter(user_id, message_content, time_to_send)
    await message.reply("Вы подписались на рассылку!")
