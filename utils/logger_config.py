import logging
import os
import datetime
import colorlog


# Создаем папку для файлов с логами, если ее нет
log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)


# Указываем правила для наименования файлов с логами
log_filename = datetime.datetime.now().strftime('%H_%M %d_#m_%y') + '.log'
log_filepath = os.path.join(log_dir, log_filename)


# Инициализация объекта логгера
logger = logging.getLogger('Token Sender')

if not logger.hasHandlers():
    # Инициализация канала вывода логов в файл
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(logging.DEBUG | logging.INFO | logging.ERROR | logging.WARNING)


    # Инициализация канала вывода логов в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO | logging.ERROR)

    # Инициализация формата вывода сообщений в логах
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s') # '%(asctime)s - %(levelname)s: %(message)s'
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s: %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'ERROR': 'red'
        }
    )

    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)