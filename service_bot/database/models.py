from sqlalchemy import String, DateTime, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from .base import Base, unique_str_an


class User(Base):
    username: Mapped[unique_str_an]
    user_id: Mapped[int]

    @classmethod
    def get_user(cls, session):
        users = session.query(cls.user_id, cls.username).all()
        return {user.user_id: user.username for user in users}

    @classmethod
    async def add_user(cls, user_id: int, username: str, session: AsyncSession):
        # Проверяем, существует ли пользователь с таким user_id в базе
        result = await session.execute(select(cls).filter_by(user_id=user_id))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ValueError(f"Пользователь с user_id={user_id} уже существует.")

        new_user = cls(username=username, user_id=user_id)
        session.add(new_user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise ValueError(f"Ошибка добавления пользователя с user_id={user_id}.")


class Newsletter(Base):
    message: Mapped[str] = mapped_column(String)
    send_at: Mapped[datetime] = mapped_column(DateTime)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user = relationship("User", backref="newsletters")

    @classmethod
    async def add_newsletter(
        cls, user_id: int, message: str, send_at: datetime, session: AsyncSession
    ):
        result = await session.execute(select(User).filter_by(user_id=user_id))
        user = result.scalars().first()

        if not user:
            raise ValueError(f"Пользователь с user_id={user_id} не найден.")

        try:
            new_newsletter = cls(user_id=user_id, message=message, send_at=send_at)
            session.add(new_newsletter)
            await session.flush()
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Ошибка при добавлении рассылки: {e}")

    @classmethod
    async def get_newsletters(cls, session: AsyncSession, current_time: datetime):
        result = await session.execute(select(cls).where(cls.send_at <= current_time))
        return result.scalars().all()
