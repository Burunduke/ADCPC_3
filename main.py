import time
import pandas as pd
from utils.core.engine_core import InvertedIndex
from utils.config import Config
from utils.logger import create_logger
from pympler import asizeof
import pickle
from pathlib import Path


logger = create_logger()

try:
    config = Config()
except ValueError as e:
    logger.exception(f"Неправильное входное значение в конфиге: {str(e)}")
    exit()
except TypeError as e:
    logger.exception(f"Неправильный тип в конфиге: {str(e)}")
    exit()
except FileNotFoundError as e:
    logger.exception(f"Файл конфига не найден: {str(e)}")
    exit()
except AttributeError as e:
    logger.exception(f"Неправильно задана дата: {str(e)}")
    exit()
except Exception as e:
    logger.exception(f"Неожиданная ошибка в конфиге: {str(e)}")
    exit()


def ensure_dir(path):
    path = Path(path)
    if not path.exists():
        logger.warning("Создется новый выходной путь. Скорее всего он будет пуст!")
        path.mkdir(parents=True, exist_ok=True)


def get_time(func, *args, **kwargs):
    """
    Вывод времени работы функции
    """
    start = time.time()
    res = func(*args, **kwargs)
    end = time.time()
    func_time = round(end - start, 6)
    return res, func_time


def get_size(some_object):
    """
    Возвращает размер объекта в килобайтах
    """
    size = asizeof.asizeof(some_object) / 1024
    return size


def main():
    logger.info("Программа запущенна")
    directory_path = "data"
    ensure_dir(directory_path)

    # загрузка данных и их соединение
    folder = Path(directory_path)
    all_csv_files = folder.glob("*.csv")
    dfs = [pd.read_csv(file) for file in all_csv_files]
    if not dfs:
        logger.exception(f"Пустая входная папка {directory_path}")
        return -1

    df = pd.concat(dfs, ignore_index=True)
    logger.info(f"Успешно загружены входные таблицы. Сэмпл: \n{df.sample(1)}")


    # формируем словарь документов: id -> текст
    documents = dict(zip(df["id"], df["text"]))

    # строим индекс
    index = InvertedIndex()

    for doc_id, text in documents.items():
        if isinstance(text, str):
            index.insert_doc(doc_id, text)

    # Сохранение индекса в файл, чтобы не строить заново каждый раз
    with open("data/inverted_index.pkl", "wb") as f:
        pickle.dump(index, f)

    with open("data/inverted_index.pkl", "rb") as f:
        index = pickle.load(f)

    logger.info(f"Размер изначального индекса: {get_size(index.get_index())}")

    # Поиск до сжатия
    for mention in config.mentions:

        result, time_of_complete = get_time(index.search, mention)

        logger.info(f"Время поиска <{mention}> в простом индексе - {time_of_complete}")

        logger.info(f"Документы, содержащие <{mention}>: {result}")
        logger.info(f"Всего их - {len(result)}")

        # пример
        for doc_id in result:
            logger.info(f"Документ {doc_id}: {index.get_doc(doc_id)}")
            break

    # Сжатие (гамма-кодирование), замер времени и размера
    with open("data/inverted_index.pkl", "rb") as f:
        index = pickle.load(f)

    logger.info(f"Время сжатия: {get_time(index.compress_index, 'gamma')}")

    logger.info(f"Размер сжатого гамма-кодированием индекса: {get_size(index.get_index())}")

    # Повторный поиск после гамма-сжатия
    for mention in config.mentions:

        result, time_of_complete = get_time(index.search, mention)

        logger.info(f"Время поиска <{mention}> в сжатом гамма-кодированием индексе - {time_of_complete}")

        logger.info(f"Документы, содержащие <{mention}>: {result}")
        logger.info(f"Всего их - {len(result)}")

    # Сжатие (дельта-кодирование), замер времени и размера
    with open("data/inverted_index.pkl", "rb") as f:
        index = pickle.load(f)

    logger.info(f"Время сжатия: {get_time(index.compress_index, 'delta')}")

    logger.info(f"Размер сжатого дельта-кодированием индекса: {get_size(index.get_index())}")

    # Повторный поиск после дельта-сжатия
    for mention in config.mentions:

        result, time_of_complete = get_time(index.search, mention)

        logger.info(f"Время поиска <{mention}> в сжатом дельта-кодированием индексе - {time_of_complete}")

        logger.info(f"Документы, содержащие <{mention}>: {result}")
        logger.info(f"Всего их - {len(result)}")


if __name__ == "__main__":
    main()
