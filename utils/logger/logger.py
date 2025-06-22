import logging


def create_logger() -> logging.Logger:
    # Создаем логгер
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)

    # --- Handler 1: лог-файл ---
    file_handler = logging.FileHandler('app.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_format)

    # --- Handler 2: консоль ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)

    # --- Подключаем хендлеры ---
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

