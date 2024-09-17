import asyncio

import requests

from app.lib.scrap_news.scrap_news import get_news


def get_html(url="https://tass.ru/ekonomika"):
    html = requests.get(url)

    with open("index.html", "a", encoding="utf-8") as file:
        file.write(html.text)


if __name__ == '__main__':
    # get_html()
    asyncio.run(get_news())
    # t1 = "123?123321"
    # t2 = "123"
    # print(t1.split("?")[0])
    # print(t2.split("?")[0])
