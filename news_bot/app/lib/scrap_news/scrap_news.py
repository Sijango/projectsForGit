import asyncio
import random

import requests

import config

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from typing import Any, Dict, List


async def get_connection(session):
    class Conn:

        rbc_news: List[Dict[str, Any]]      # Предварительный набор новостей по рбк
        forklog_news: List[Dict[str, Any]]  # Предварительный набор новостей по форклог
        frankrg_news: List[Dict[str, Any]]  # Предварительный набор новостей по франкрг
        forbes_news: List[Dict[str, Any]]   # Предварительный набор новостей по forbes
        tass_news: List[Dict[str, Any]]     # Предварительный набор новостей по tass

        __tmp_rbc_urls: Dict[str, Any]      # Список url-адресов для новостей по рбк
        __tmp_forklog_urls: Dict[str, Any]  # Список url-адресов для новостей по форклог
        __tmp_frankrg_urls: Dict[str, Any]  # Список url-адресов для новостей по франкрг
        __tmp_forbes_urls: Dict[str, Any]   # Список url-адресов для новостей по forbes
        __tmp_tass_urls: Dict[str, Any]     # Список url-адресов для новостей по tass

        __tmp_rbc_urls_from_file: List[str]      # Список url-адресов для новостей по рбк
        __tmp_forklog_urls_from_file: List[str]  # Список url-адресов для новостей по форклог
        __tmp_frankrg_urls_from_file: List[str]  # Список url-адресов для новостей по франкрг
        __tmp_forbes_urls_from_file: List[str]   # Список url-адресов для новостей по forbes
        __tmp_tass_urls_from_file: List[str]     # Список url-адресов для новостей по tass

        def __init__(self, ses):
            self.session = ses

            self.rbc_news = []
            self.forklog_news = []
            self.frankrg_news = []
            self.forbes_news = []
            self.tass_news = []

            self.__tmp_rbc_urls = {}
            self.__tmp_forklog_urls = {}
            self.__tmp_frankrg_urls = {}
            self.__tmp_forbes_urls = {}
            self.__tmp_tass_urls = {}

            self.__tmp_rbc_urls_from_file = open(config.PATH_TO_OLD_RBC_URLS, "r", encoding="utf-8").read().split("\n")
            self.__tmp_forklog_urls_from_file = open(config.PATH_TO_OLD_FORKLOG_URLS, "r", encoding="utf-8").read().split("\n")
            self.__tmp_frankrg_urls_from_file = open(config.PATH_TO_OLD_FRANK_URLS, "r", encoding="utf-8").read().split("\n")
            self.__tmp_forbes_urls_from_file = open(config.PATH_TO_OLD_FORBES_URLS, "r", encoding="utf-8").read().split("\n")
            self.__tmp_tass_urls_from_file = open(config.PATH_TO_OLD_TASS_URLS, "r", encoding="utf-8").read().split("\n")

        async def collect_data(self):
            task_1 = asyncio.create_task(self.get_rbc_news_urls())
            task_2 = asyncio.create_task(self.get_forklog_news_urls())
            task_3 = asyncio.create_task(self.get_frankrg_news_urls())
            task_4 = asyncio.create_task(self.get_forbes_news_urls())
            task_5 = asyncio.create_task(self.get_tass_news_urls())

            await task_1
            await task_2
            await task_3
            await task_4
            await task_5

            # print(f"__tmp_rbc_urls_from_file: {self.__tmp_rbc_urls_from_file}")
            with open(config.PATH_TO_OLD_RBC_URLS, "w", encoding="utf-8") as file:
                file.write("\n".join(self.__tmp_rbc_urls_from_file))

            # print(f"__tmp_forklog_urls_from_file: {self.__tmp_forklog_urls_from_file}")
            with open(config.PATH_TO_OLD_FORKLOG_URLS, "w", encoding="utf-8") as file:
                file.write("\n".join(self.__tmp_forklog_urls_from_file))

            # print(f"__tmp_frankrg_urls_from_file: {self.__tmp_frankrg_urls_from_file}")
            with open(config.PATH_TO_OLD_FRANK_URLS, "w", encoding="utf-8") as file:
                file.write("\n".join(self.__tmp_frankrg_urls_from_file))

            with open(config.PATH_TO_OLD_FORBES_URLS, "w", encoding="utf-8") as file:
                file.write("\n".join(self.__tmp_forbes_urls_from_file))

            with open(config.PATH_TO_OLD_TASS_URLS, "w", encoding="utf-8") as file:
                file.write("\n".join(self.__tmp_tass_urls_from_file))

            result_news = {
                "rbc": self.rbc_news,
                "forklog": self.forklog_news,
                "frankrg": self.frankrg_news,
                "forbes": self.forbes_news,
                "tass": self.tass_news
            }

            return result_news

        async def get_rbc_news_urls(self):
            try:
                for rbc_url in config.URLS[0]["URL"]:
                    async with self.session.get(rbc_url, timeout=10) as response:
                        data = await response.text()

                        soup = BeautifulSoup(data, 'lxml')
                        cards = soup.find_all("div", {"class": "q-item js-load-item js-index-central-column-main"})

                        for card in cards:
                            try:
                                url = card.find('a', {"class": "q-item__link js-yandex-counter js-index-central-column-io js-rm-central-column-item js-central-column-from-param"}).get("href")
                                name = " ".join(card.find("span", {"class": "q-item__title js-rm-central-column-item-text"}).text.replace("\n", "").split())

                                if url not in self.__tmp_rbc_urls_from_file:
                                    self.__tmp_rbc_urls[url] = name
                                    self.__tmp_rbc_urls_from_file.append(url)
                                else:
                                    continue
                                    # print("tut-RBc")
                                    # self.__tmp_rbc_urls_from_file.append(url)

                            except:
                                continue

                # print(self.__tmp_rbc_urls)
                await self.__get_rbc_news_data()
            except:
                print(">>>>>>>>>>>>>>>>>>>>>")
                print("[SYS] RBC Недоступен!")
                print("<<<<<<<<<<<<<<<<<<<<<")

        async def get_forklog_news_urls(self):
            try:
                for forklog_url in config.URLS[1]["URL"]:
                    async with self.session.get(forklog_url, timeout=10) as response:
                        data = await response.text()

                        soup = BeautifulSoup(data, 'lxml')
                        # top_card = soup.find("div", {"class": "cell has_trending"})
                        # cards = soup.find_all("div", {"class": "cell"})
                        #
                        # top_url = top_card.find("a").get("href")
                        # top_name = top_card.find("div", {"class": "text_blk"}).find("p").text.replace("\n", "")
                        #
                        # if top_url not in self.__tmp_forklog_urls_from_file:
                        #     self.__tmp_forklog_urls[top_url] = top_name
                        # else:
                        #     self.__tmp_forklog_urls_from_file.append(top_url)
                        cards = soup.find("div", {"class": "posts_wrap"}).find("div", {"class": "category_page_grid"}).find_all("div", {"class": "cell"})
                        for card in cards:
                            try:
                                url = card.find("div", {"class": "post_item"}).find("a").get("href")
                                name = card.find("div", {"class": "post_item"}).find("a").find("div", {"class": "text_blk"}).find("p").text.replace("\n", "")

                                # if "?doing_wp_cron=1686894569.2636001110076904296875" not in url:
                                #     if url+"?doing_wp_cron=1686894569.2636001110076904296875" not in self.__tmp_forklog_urls_from_file:
                                #         self.__tmp_forklog_urls[url] = name
                                #         self.__tmp_forklog_urls_from_file.append(url+"?doing_wp_cron=1686894569.2636001110076904296875")
                                #     else:
                                #         continue
                                # else:
                                #     if url not in self.__tmp_forklog_urls_from_file:
                                #         self.__tmp_forklog_urls[url] = name
                                #         self.__tmp_forklog_urls_from_file.append(url)
                                #     else:
                                #         continue

                                if url.split("?")[0] not in self.__tmp_forklog_urls_from_file:
                                    self.__tmp_forklog_urls[url] = name
                                    self.__tmp_forklog_urls_from_file.append(url)
                                else:
                                    continue

                            except:
                                continue

                # print(self.__tmp_forklog_urls)
                await self.__get_forklog_news_data()

            except:
                print(">>>>>>>>>>>>>>>>>>>>>")
                print("[SYS] Forklog Недоступен!")
                print("<<<<<<<<<<<<<<<<<<<<<")

        async def get_frankrg_news_urls(self):
            try:
                for frankrg_url in config.URLS[2]["URL"]:
                    async with self.session.get(frankrg_url, timeout=10) as response:
                        data = await response.text()

                        soup = BeautifulSoup(data, 'lxml')
                        cards = soup.find("ul", {"class": "grid grid-tag grid-ajax"}).find_all("li", {"class": "item"})

                        for card in cards:
                            try:
                                # print("rur")
                                url = card.find("div", {"class": "h4"}).find("a").get("href")
                                name = " ".join(card.find("div", {"class": "h4"}).find("a").text.replace("\n", "").split())

                                if url not in self.__tmp_frankrg_urls_from_file:
                                    self.__tmp_frankrg_urls[url] = name
                                    self.__tmp_frankrg_urls_from_file.append(url)
                                else:
                                    continue

                            except:
                                continue

                # print(self.__tmp_frankrg_urls)
                await self.__get_frankrg_news_data()
            except:
                print(">>>>>>>>>>>>>>>>>>>>>")
                print("[SYS] Frank Media Недоступна!")
                print("<<<<<<<<<<<<<<<<<<<<<")

        async def get_tass_news_urls(self):
            try:
                for tass_url in config.URLS[4]["URL"]:
                    async with self.session.get(tass_url, timeout=10) as response:
                        data = await response.text()

                        soup = BeautifulSoup(data, 'lxml')
                        cards = soup.find("main", {"class": "PageLayout_main__0L_YP"}).find("div", {"class": "Search_search_page__lRjKD"}).\
                            find("div", {"class": "Listing_list__qKmtM"}).find_all("a", {"class", "tass_pkg_link-v5WdK"})

                        for card in cards:
                            try:
                                    # print("rur")
                                url = card.get("href")
                                # name = " ".join(card.find("div", {"class": "tass_pkg_card-3XeRZ tass_pkg_card--no_media-sigQi"}).\
                                #                 find("div", {"class": "tass_pkg_card__left-c34PL tass_pkg_card__left--no_media-GqTHq"}).\
                                #                 find("div", {"class": "tass_pkg_title_wrapper-i0jgn"}).find("span", {"class": "ds_ext_title-1XuEF ds_ext_title--inline-TH8tk ds_ext_title--font_weight_medium-7lN1- ds_ext_title--variant_h2_extra_large-O5fUc ds_ext_title--color_primary-MLP6K"}).text.replace("\n", "").split())

                                # print(url)
                                if f"https://tass.ru/{url}" not in self.__tmp_tass_urls_from_file:
                                    self.__tmp_tass_urls[f"https://tass.ru/{url}"] = f"https://tass.ru/{url}"
                                    self.__tmp_tass_urls_from_file.append(f"https://tass.ru/{url}")
                                else:
                                    continue

                            except Exception as ex:
                                print(ex)
                                continue

                # print(self.__tmp_tass_urls)
                await self.__get_tass_news_data()
            except:
                print(">>>>>>>>>>>>>>>>>>>>>")
                print("[SYS] Tass Недоступна!")
                print("<<<<<<<<<<<<<<<<<<<<<")

        async def get_forbes_news_urls(self):
            try:
                for forbes_url in config.URLS[3]["URL"]:
                    async with self.session.get(forbes_url, timeout=10) as response:
                        data = await response.text()

                        soup = BeautifulSoup(data, 'lxml')
                        top_cards = soup.find("div", {"class": "_3wyym"}).\
                            find("div", {"class": "_2ThAc _637S0"})
                        cards = top_cards.find_all("div", {"class": "_3dtP5"})

                        for card in cards:
                            top_or_not = card.find("div", {"class": "_2npuA"})
                            # print("p1")
                            # print(top_or_not.text)
                            try:
                                if top_or_not:
                                    top_url = card.find("div", {"class": "_2npuA"}).find("div", {"class": "_2nkB1"}).find("a", {"class": "_1QIeJ"}).get("href")
                                    top_name = card.find("div", {"class": "_2npuA"}).find("div", {"class": "_2nkB1"}).find("a", {"class": "_1QIeJ"}).\
                                        find("div", {"class": "_1rha2"}).find("div", {"class": "_1fQ6O"}).text
                                    # print(top_url)

                                else:
                                    top_or_not = card.find("div", {"class": "laBq1"}).find("div", {"class": "_3Sgj7"}).find(
                                        "a", {"class": "_3eGVH"}).find("div", {"class": "_2iYJc"})

                                    if top_or_not:
                                        top_url = card.find("div", {"class": "laBq1"}).find("div", {"class": "_3Sgj7"}).find(
                                            "a", {"class": "_3eGVH"}).get("href")
                                        top_name = card.find("div", {"class": "laBq1"}).find("div", {"class": "_3Sgj7"}).find(
                                            "a", {"class": "_3eGVH"}).find("div", {"class": "_2iYJc"}).find("span").text
                                    else:
                                        top_url = card.find("div", {"class": "laBq1"}).find("div", {"class": "_3Sgj7"}).find(
                                            "a", {"class": "_3eGVH"}).get("href")
                                        top_name = card.find("div", {"class": "laBq1"}).find("div", {"class": "_3Sgj7"}).find(
                                            "a", {"class": "_3eGVH"}).find("p", {"class": "_3Ew4G"}).find("span").text

                                if f"https://www.forbes.ru{top_url}" not in self.__tmp_forbes_urls_from_file:
                                    self.__tmp_forbes_urls[f"https://www.forbes.ru{top_url}"] = top_name
                                    self.__tmp_forbes_urls_from_file.append(f"https://www.forbes.ru{top_url}")
                                else:
                                    continue
                            except:
                                continue

                # print(self.__tmp_forklog_urls)
                await self.__get_forbes_news_data()

            except:
                print(">>>>>>>>>>>>>>>>>>>>>")
                print("[SYS] Forbes Недоступен!")
                print("<<<<<<<<<<<<<<<<<<<<<")

        async def __get_forbes_news_data(self):
            for url in self.__tmp_forbes_urls.keys():
                text = []
                try:
                    async with self.session.get(f"{url}", timeout=10) as response:
                        data = await response.text()
                        soup = BeautifulSoup(data, 'lxml')

                        card = soup.find("div", {"class", "wERSY"}).find("div", {"class": "_3wyym"}).\
                            find("article").find("div", {"class": "IVHFK"})

                        # print(card)

                        title = card.find("div", {"class": "_3J9Ic"}).find("div", {"class": "_3o-RD"}).find("h1").text
                        title = " ".join(title.split())
                        # print(title)
                        p_classes = card.find("div", {"class": "_2LS9B"}).find("div", {"class": "_1eYTt"}).find_all("p", {"class": "yl27R _10zjs"})
                        # p_classes = soup.find("div", {"class": "article__text article__text_free"}).find_all("p")
                        count = 0
                        count_symbols = 0
                        for p in p_classes:
                            count += 1
                            if count <= random.randint(3, 6):
                                tmp = " ".join(p.find("span").text.split())
                                tmp = tmp.strip()

                                count_symbols += len(tmp)
                                if len(tmp) >= 90 and count_symbols < 850:
                                    text.append(tmp)

                        text = "\n\n".join(text)

                    self.forbes_news.append({
                        "title": title,
                        "text": text,
                        "url": url
                    })
                except Exception as ex:
                    print(f"Forbes: {ex}")

            # print(self.forbes_news)

        async def __get_rbc_news_data(self):
            for url in self.__tmp_rbc_urls.keys():
                text = []
                try:
                    async with self.session.get(url, timeout=10) as response:
                        data = await response.text()
                        soup = BeautifulSoup(data, 'lxml')
                        title = soup.find("div", {"class": "article__header__title"}).find("h1", {"class": "article__header__title-in js-slide-title"}).text
                        title = " ".join(title.split())

                        p_classes = soup.find("div", {"class": "article__text article__text_free"}).find_all("p")
                        count = 0
                        count_symbols = 0
                        for p in p_classes:
                            count += 1
                            if count <= random.randint(3, 6):
                                tmp = " ".join(p.text.split())
                                tmp = tmp.strip()

                                count_symbols += len(tmp)
                                if len(tmp) >= 90 and count_symbols < 850:
                                    text.append(tmp)

                        text = "\n\n".join(text)

                    self.rbc_news.append({
                        "title": title,
                        "text": text,
                        "url": url
                    })
                except Exception as ex:
                    print(f"RBC: {ex}")

            # print(self.rbc_news)

        async def __get_tass_news_data(self):
            for url in self.__tmp_tass_urls.keys():
                text = []
                try:
                    async with self.session.get(url, timeout=10) as response:
                        data = await response.text()
                        soup = BeautifulSoup(data, 'lxml')
                        card = soup.find("main", {"class": "PageLayout_main__0L_YP"}).find("section", {"class": "Material_container__ETnUZ"})

                        title = card.find("div", {"class": "NewsHeader_upper_text_block__oUUSZ"}).find("h1", {"class": "ds_ext_title-1XuEF"}).text
                        title = " ".join(title.split())

                        p_classes = card.find("article").find_all("p", {"class": "Paragraph_paragraph__nYCys"})
                        count = 0
                        count_symbols = 0
                        for p in p_classes:
                            count += 1
                            if count <= random.randint(3, 6):
                                tmp = " ".join(p.find("span", {"class": "ds_ext_text-tov6w"}).text.split())
                                if "/ТАСС/. " in tmp:
                                    tmp = tmp.split("/ТАСС/. ")[1]

                                tmp = tmp.strip()

                                count_symbols += len(tmp)
                                if len(tmp) >= 90 and count_symbols < 850:
                                    text.append(tmp)

                        text = "\n\n".join(text)

                    self.tass_news.append({
                        "title": title,
                        "text": text,
                        "url": url
                    })
                except Exception as ex:
                    print(f"Tass: {ex}")

            # print(self.tass_news)

        async def __get_forklog_news_data(self):
            for url in self.__tmp_forklog_urls.keys():
                text = []
                try:
                    async with self.session.get(url, timeout=10) as response:
                        data = await response.text()
                        soup = BeautifulSoup(data, 'lxml')

                        post = soup.find("div", {"class": "post_content"})
                        title = post.find("h1").text.replace('\u00A0', '')
                        # title = " ".join(title.split())

                        p_classes = post.find_all("p")

                        count = 0
                        count_symbols = 0
                        for p in p_classes:
                            if self._check_p(p.text):
                                continue

                            count += 1
                            if count <= random.randint(3, 6):
                                tmp = " ".join(p.text.split())
                                tmp = tmp.replace('\u00A0', '').strip()

                                count_symbols += len(tmp)
                                if len(tmp) >= 90 and count_symbols < 850:
                                    text.append(tmp)

                        text = "\n\n".join(text)

                    self.forklog_news.append({
                        "title": title,
                        "text": text,
                        "url": url
                    })
                except Exception as ex:
                    print(f"Forklog: {ex}")

            # print(self.forklog_news)

        @staticmethod
        def _check_p(text):
            if "/" in text:
                return True
            if "https" in text:
                return True
            if "@" in text:
                return True
            if "http" in text:
                return True

            return False

        async def __get_frankrg_news_data(self):
            for url in self.__tmp_frankrg_urls.keys():
                try:
                    async with self.session.get(url, timeout=10) as response:
                        data = await response.text()
                        soup = BeautifulSoup(data, 'lxml')

                        post = soup.find("div", {"class": "page-post__container svelte-1rrrj2u"})\
                            .find("div", {"class": "page-post__parts svelte-1rrrj2u"})\
                            .find("div").find("div", {"class": "page-post__part svelte-1rrrj2u"})\
                            .find("div", {"class": "page-post__main svelte-1rrrj2u"})\
                            .find("div", {"class": "page-post__article svelte-1rrrj2u"})\
                            .find("div", {"class": "svelte-1rkhtzt"})\
                            .find("div", {"class": "widget svelte-16se9u9"})\
                            .find("div", {"class": "widget__container svelte-16se9u9"})\
                            .find("div", {"class": "post svelte-1rkhtzt"})

                        title = post.find("h1", {"class": "post__title svelte-1rkhtzt"}).text.replace('\u00A0', '')
                        paragraphs = post.find("div", {"class": "post__body svelte-1rkhtzt"}).find("div", {"class": "post-content svelte-p9gh0l"}).find_all("p")

                        text = []
                        count = 0
                        count_symbols = 0
                        for p_text in paragraphs:
                            count += 1
                            if count <= random.randint(3, 6):
                                tmp = p_text.text.replace('\u00A0', '').strip()

                                count_symbols += len(tmp)
                                if len(tmp) >= 90 and count_symbols < 850:
                                    text.append(tmp)

                        text = "\n\n".join(text)

                    self.frankrg_news.append({
                        "title": title,
                        "text": text,
                        "url": url
                    })
                except Exception as ex:
                    print(f"Frankrg: {ex}")

            # print(self.frankrg_news)

    return Conn(session)


class ScrapNews:
    def __init__(self):
        pass

    async def get_news(self):
        pass

    async def __aenter__(self):
        self.session = ClientSession()
        self.conn = await get_connection(self.session)

        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


async def get_news():
    async with ScrapNews() as conn:
        # task_1 = asyncio.create_task(conn.get_rbc_news_urls())
        # task_2 = asyncio.create_task(conn.get_forklog_news_urls())
        # task_3 = asyncio.create_task(conn.get_frankrg_news_urls())

        # await task_1
        # await task_2
        # await task_3
        task = asyncio.create_task(conn.collect_data())
        result_data = await task

    # print(result_data)
    return result_data


if __name__ == '__main__':
    asyncio.run(get_news())
    # html = get_html("https://frankmedia.ru/122017")
    # with open("index1.html", "w", encoding="utf-8") as file:
    #     file.write(html)
