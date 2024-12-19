import pytest
from aiogram.types import Message
from unittest.mock import MagicMock
from service_bot.core.message_handler import send_welcome, send_help, echo


@pytest.fixture
def mock_bot():
    bot = MagicMock()
    return bot


@pytest.mark.asyncio
async def test_send_welcome(mock_bot):
    message = MagicMock(spec=Message)
    message.reply = MagicMock()
    await send_welcome(message)
    message.reply.assert_called_once_with("Привет! Я ваш автотвечик. Чем могу помочь?")


@pytest.mark.asyncio
async def test_send_help(mock_bot):
    message = MagicMock(spec=Message)
    message.reply = MagicMock()
    await send_help(message)
    message.reply.assert_called_once_with(
        "Я могу ответить на ваши вопросы и помочь с услугами. Напишите мне, и я постараюсь вам помочь!"
    )


@pytest.mark.asyncio
async def test_echo(mock_bot):
    message = MagicMock(spec=Message)
    message.reply = MagicMock()
    message.text = "Тест"
    await echo(message)
    message.reply.assert_called_once_with(
        text="Спасибо за ваш выбор! Мы свяжемся с вами в ближайшее время"
    )
