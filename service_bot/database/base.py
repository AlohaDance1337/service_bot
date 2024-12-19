from datetime import datetime
from typing import Annotated
from sqlalchemy import Integer, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from service_bot.tools import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(
    url=DATABASE_URL, echo=True
)  # echo=True для логирования запросов

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

unique_str_an = Annotated[str, mapped_column(unique=True)]


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                allowed_kwargs = method.__code__.co_varnames
                kwargs = {
                    key: value for key, value in kwargs.items() if key in allowed_kwargs
                }
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откат транзакции при ошибке
                raise e
            finally:
                await session.close()  # Закрытие сессии

    return wrapper


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True  # Указываем, что класс абстрактный и не создает таблицу

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # Динамическое создание имени таблицы
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
