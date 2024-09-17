import json
import os

CONFIG_FILE = json.load(open("config.json", encoding="utf-8"))

TOKEN = CONFIG_FILE["token"]
CHATS = CONFIG_FILE["chats"]
ADMINS = CONFIG_FILE['admins']
CATEGORIES = CONFIG_FILE["categories"]
URLS = CONFIG_FILE["URL"]
INTERVAL = CONFIG_FILE["interval"]
SEND_TO_CHATS = CONFIG_FILE["send_to_chat"]
FOOTER = CONFIG_FILE["footer_in_message"]
IMAGES_VISION = CONFIG_FILE["img"]["vision"]

PATH_TO_OLD_RBC_URLS = "src/.tmp_data/rbc_urls.txt"
PATH_TO_OLD_FORKLOG_URLS = "src/.tmp_data/forklog_urls.txt"
PATH_TO_OLD_FRANK_URLS = "src/.tmp_data/frank_urls.txt"
PATH_TO_OLD_FORBES_URLS = "src/.tmp_data/forbes_urls.txt"
PATH_TO_OLD_TASS_URLS = "src/.tmp_data/tass_urls.txt"


if not os.path.exists("src"):
    os.mkdir("src")

if not os.path.exists("src/.tmp_data"):
    os.mkdir("src/.tmp_data")

if not os.path.exists("src/.tmp_data/forklog_urls.txt"):
    open("src/.tmp_data/forklog_urls.txt", "x").close()

if not os.path.exists("src/.tmp_data/frank_urls.txt"):
    open("src/.tmp_data/frank_urls.txt", "x").close()

if not os.path.exists("src/.tmp_data/rbc_urls.txt"):
    open("src/.tmp_data/rbc_urls.txt", "x").close()

if not os.path.exists("src/.tmp_data/forbes_urls.txt"):
    open("src/.tmp_data/forbes_urls.txt", "x").close()

if not os.path.exists("src/.tmp_data/tass_urls.txt"):
    open("src/.tmp_data/tass_urls.txt", "x").close()


def get_config_file():
    config_file = json.load(open("config.json"))
    return config_file


# ,
#       "vision/MacBook Pro 14_ - 1.jpg",
#       "vision/MacBook Pro 14_ - 2.jpg",
#       "vision/MacBook Pro 14_ - 3.jpg",
#       "vision/MacBook Pro 14_ - 4.jpg",
#       "vision/MacBook Pro 14_ - 5.jpg",
#       "vision/MacBook Pro 14_ - 6.jpg",
#       "vision/MacBook Pro 14_ - 7.jpg",
#       "vision/MacBook Pro 14_ - 8.jpg",
#       "vision/MacBook Pro 14_ - 9.jpg",
#       "vision/MacBook Pro 14_ - 10.jpg",
#       "vision/MacBook Pro 14_ - 11.jpg",
#       "vision/MacBook Pro 14_ - 12.jpg",
#       "vision/MacBook Pro 14_ - 13.jpg",
#       "vision/MacBook Pro 14_ - 14.jpg",
#       "vision/MacBook Pro 14_ - 15.jpg",
#       "vision/MacBook Pro 14_ - 16.jpg",
#       "vision/MacBook Pro 14_ - 17.jpg",
#       "vision/MacBook Pro 14_ - 18.jpg",
#       "vision/MacBook Pro 14_ - 19.jpg",
#       "vision/MacBook Pro 14_ - 20.jpg",
#       "vision/MacBook Pro 14_ - 21.jpg",
#       "vision/MacBook Pro 14_ - 22.jpg",
#       "vision/MacBook Pro 14_ - 23.jpg",
#       "vision/MacBook Pro 14_ - 24.jpg",
#       "vision/MacBook Pro 14_ - 25.jpg",
#       "vision/MacBook Pro 14_ - 26.jpg",
#       "vision/MacBook Pro 14_ - 27.jpg",
#       "vision/MacBook Pro 14_ - 28.jpg",
#       "vision/MacBook Pro 14_ - 29.jpg",
#       "vision/MacBook Pro 14_ - 30.jpg",
#       "vision/MacBook Pro 14_ - 31.jpg",
#       "vision/MacBook Pro 14_ - 32.jpg",
#       "vision/MacBook Pro 14_ - 33.jpg",
#       "vision/MacBook Pro 14_ - 34.jpg",
#       "vision/MacBook Pro 14_ - 35.jpg",
#       "vision/MacBook Pro 14_ - 36.jpg"

# def set_json_in_config_file(json_data):
#     with open("../config2.json", "w", encoding="utf-8") as f:
#         json.dump(json_data, f)
#
#
# json_d = """
# {
#   "token": "5562820909:AAGp6GzNG6syrm2_-1w6LJQq57OoMJ7hgnM",
#
#   "chats": [
#     "-1001515492100"
#   ],
#
#   "admins": [
#     "123"
#   ],
#
#   "categories": [
#     ""
#   ]
# }
# """
#
# if __name__ == '__main__':
#     set_json_in_config_file(json_d)
#     print(get_config_file())
