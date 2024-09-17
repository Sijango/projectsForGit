from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_markup(message_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    markup.add(InlineKeyboardButton(f"Выпустить", callback_data=message_id))

    return markup


