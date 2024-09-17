from typing import List

from aiogram import Dispatcher, types
from app.handlers import messages


async def start_ans(message: types.Message):
    await message.answer(messages.START_MESSAGE)
    await message.bot.delete_message(message.chat.id, message.message_id)


async def help_ans(message: types.Message):
    await message.answer(messages.HELP_MESSAGE)
    await message.bot.delete_message(message.chat.id, message.message_id)


def register_handlers_basic(dp: Dispatcher, admins: List[str]):
    dp.register_message_handler(start_ans,
                                lambda message: str(message.from_user.id) in admins,
                                commands='start',
                                state="*")
    dp.register_message_handler(help_ans,
                                lambda message: str(message.from_user.id) in admins,
                                commands='help',
                                state="*")

