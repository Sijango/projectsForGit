import os
import smtplib
import time
import json

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.header import Header

from excel_reader import ExcelReader

PATH_TO_CONFIG = 'data/config.json'
CONFIG = json.load(open(PATH_TO_CONFIG, 'r', encoding="utf-8"))
# pyinstaller --onefile --noconfirm --console --name EmailSender C:\projects\EmailSender\main.py

# Настройки
SMTP_SERVER = CONFIG["smtp"]["server"]
SMTP_PORT = CONFIG["smtp"]["port"]
USERNAME = CONFIG["email_from"]["username"]

# Получатель, тема и тело письма
# TO_EMAIL = 'recipient@example.com'
SUBJECT = CONFIG["msg"]["subject"]
BODY = CONFIG["msg"]["body"]

# Работа с файлом:
PATH_TO_EXCEL_FILE = CONFIG["path_to_file_excel"]
PATH_TO_POWER_POINT_FILE = CONFIG["path_to_file_power_point"]


def read_excel():
    converter = ExcelReader(PATH_TO_EXCEL_FILE)

    status, error_msg = converter.initial_dataframe()
    if not status:
        print(error_msg)
        exit()

    status, df = converter.start()
    if not status:
        print(df)
        time.sleep(10)
        exit()

    return df


def add_file_to_msg(msg, filename):
    try:
        # Проверяем, существует ли файл
        if not os.path.isfile(filename):
            raise FileNotFoundError(f'Файл не найден: {filename}')

        with open(filename, 'rb') as attachment:
            # Определяем тип контента на основе расширения файла
            part = MIMEBase('application', 'vnd.openxmlformats-officedocument.presentationml.presentation')  # Для .pptx
            part.set_payload(attachment.read())
            encoders.encode_base64(part)

            # Используем os.path.basename для получения имени файла
            filename_base = os.path.basename(filename)
            encoded_filename = Header(filename_base, 'utf-8').encode()
            part.add_header('Content-Disposition',
                            f'attachment; filename={encoded_filename}; filename*=UTF-8\'\'{filename_base}')

            msg.attach(part)

        return msg

    except FileNotFoundError as fnf_error:
        print(f'Ошибка: {fnf_error}')
        time.sleep(10)
        exit()
    except Exception as e:
        print(f'Ошибка при открытии файла {filename}: {e}')
        time.sleep(10)
        exit()


def send_msg(msg, email):
    # Отправка письма
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    try:
        server.ehlo()
        # server.starttls()  # Установка защищенного соединения
        # server.login(USERNAME, PASSWORD)
        server.send_message(msg)
        print(f'Письмо успешно отправлено на {email}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')
        time.sleep(10)
        exit()
    finally:
        server.quit()  # Закрываем соединение


def main():
    df = read_excel()

    for _, data in df.iterrows():
        msg = MIMEMultipart()
        msg['From'] = USERNAME
        msg['To'] = data["Электронная почта"]
        msg['Subject'] = SUBJECT
        msg.attach(MIMEText(BODY.format(fio=data["ФИО руководителя"]), 'plain'))
        msg = add_file_to_msg(msg, PATH_TO_POWER_POINT_FILE)
        send_msg(msg, data["Электронная почта"])


if __name__ == '__main__':
    try:
        main()
        time.sleep(10)
    except Exception as e:
        print(e)
        time.sleep(10)
