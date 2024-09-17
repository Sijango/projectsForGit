import datetime
import json
import random
import time
import os

from sched import scheduler
from typing import List

from aiogram import Dispatcher, types
from aiogram.utils.markdown import hlink

# from app.bot.messages import messages

import config
from app import keyboards
from app.lib.images.image import ConvertImage
from app.lib.scrap_news.scrap_news import get_news


# CONFIG = load_config()


async def send_data(dp: Dispatcher):
    news = await get_news()

    for news_key in news.keys():
        for post in news[news_key]:
            title = f"<b>{post['title']}</b>\n\n"
            post_text = f"{post['text']}\n\n"
            url = f"{post['url']}"

            _message = title + post_text + url
            time.sleep(3)
            try:
                id_markup = str(random.randint(0, 10000000000000000000000000000000000))
                id_rand_photo = random.randint(0, len(config.IMAGES_VISION))

                date = datetime.datetime.now().strftime('%d%m%Y%H%M%S%f')[:-3]

                photo = ConvertImage(
                    title=post['title'],
                    _path_to_image=f"src/images/{config.IMAGES_VISION[id_rand_photo]}",
                    _path_to_save_image=f"src/tmp_img/{date}.png",
                    _path_to_font="src/fonts/Gilroy-ExtraBold.ttf",
                    font_size_title=44
                )
                photo.convert_image()
                photo.save_image()

                # await dp.bot.send_message(
                #     chat_id=config.CHATS,
                #     text=_message.replace("\n\n\n", "\n"),
                #     parse_mode='HTML',
                #     disable_notification=True,
                #     disable_web_page_preview=True,
                #     reply_markup=keyboards.gen_markup(id_markup)
                # )
                with open(f"src/tmp_img/{date}.png", "rb") as photo_to_send:
                    await dp.bot.send_photo(
                        chat_id=config.CHATS,
                        caption=_message.replace("\n\n\n", "\n"),
                        photo=photo_to_send,
                        parse_mode='HTML',
                        disable_notification=True,
                        reply_markup=keyboards.gen_markup(id_markup)
                    )

                os.remove(f"src/tmp_img/{date}.png")

            except Exception as ex:
                print(ex)
                time.sleep(40)
                continue

        # await send_last_message(dp, chat, messages_urls, date)


async def send_to_chat(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()

    chat_id = config.SEND_TO_CHATS
    text = callback.message.caption
    convert_text = text.split("\n")

    convert_text[0] = f"<b>{convert_text[0]}</b>"
    url_news = hlink("Источник", f"{convert_text[-1]}")
    url_news = f"<i>{url_news}</i>"

    url_command = hlink("VISION", f"https://vision-concierge.com/")
    url_command = f"<b>Команда {url_command}</b>"
    convert_text[-1] = f"{url_news}\n\n{url_command}"

    text = "\n".join(convert_text)
    photo = callback.message.photo

    await callback.bot.send_photo(
        chat_id=chat_id,
        caption=text,
        photo=photo[-1]["file_id"],
        parse_mode='HTML',
        # disable_notification=True,
        # disable_web_page_preview=True
    )

    # await callback.bot.send_message(
    #     chat_id=chat_id,
    #     text=text,
    #     parse_mode='HTML',
    #     # disable_notification=True,
    #     disable_web_page_preview=True
    # )


def register_handlers_send(dp: Dispatcher, admins: List[str]):
    dp.register_message_handler(send_data,
                                lambda message: str(message.from_user.id) in admins,
                                commands='get',
                                state="*")

    dp.register_callback_query_handler(send_to_chat,
                                       lambda message: str(message.from_user.id) in admins,
                                       lambda callback: callback.data not in ['get'],
                                       state="*")


