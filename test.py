from utils.core import InvertedIndex
from utils.core import EliasCoder
from pympler import asizeof
from bitarray import bitarray
from utils.logger import create_logger

index_test = InvertedIndex()
logger = create_logger()

def start():
    # Демонстрация лемматизации и токенизации
    sentence = "Переменная обозначается буквой x."
    logger.info(sentence)

    tokenized_sentence = index_test._tokenize(text=sentence)
    logger.info(f"После разбиения на токены: {tokenized_sentence}")

    lemmatized_sentence = index_test._lemmatize(tokens=tokenized_sentence)
    logger.info(f"После разбиения на токены: {lemmatized_sentence}")

    # индексирование
    # 10 предложений для тестирования сгенерированы с помощью LLM
    index_test.insert_doc(1, "Чтобы найти корни квадратного уравнения, нужно воспользоваться формулой дискриминанта.")
    index_test.insert_doc(2, "Алгебра тесно связана с другими разделами математики, включая геометрию и анализ.")
    index_test.insert_doc(3, "Переменные обозначают неизвестные величины, значения которых необходимо определить.")
    index_test.insert_doc(4, "Геометрия исследует свойства фигур и пространственные отношения.")
    index_test.insert_doc(5, "Алгебраические выражения состоят из чисел, переменных и операций над ними.")
    index_test.insert_doc(6, "График линейной функции представляет собой прямую на координатной плоскости.")
    index_test.insert_doc(7, "Статистика позволяет анализировать и интерпретировать данные.")
    index_test.insert_doc(8, "Преобразование выражений позволяет упростить вычисления и сделать решение задачи более наглядным.")
    index_test.insert_doc(9, "Математическая логика формулирует правила и принципы рассуждения.")
    index_test.insert_doc(10, "При раскрытии скобок важно правильно учитывать знаки перед ними.")

    # поиск по ключевому слову
    query = "анализ"
    results = index_test.search(query)
    logger.info(f"Документы, содержащие {query}: {results}")

    # извлечение документа
    for doc_id in results:
        logger.info(f"Документ {doc_id}:\n{index_test.get_doc(doc_id)}\n")


    coder = EliasCoder()

    # гамма-кодирование
    for number in [15, 19, 25, 27]: # 0001111 000010011 000011001 000011011
        gamma_number = coder.gamma_encoding(number)
        logger.info(f"Число {number}, гамма-представление: {gamma_number}")

    # гамма-декодирование
    for number in [109828, 20929, 2010, 1]:
        gamma_decoded_number = coder.gamma_decoding(coder.gamma_encoding(number))
        logger.info(f"Число {number}, гамма-декодированное число: {gamma_decoded_number}")


    # дельта-кодирование
    for number in [7, 8, 9]: # 01111 00100000 00100001
        delta_number = coder.delta_encoding(number)
        logger.info(f"Число {number}, дельта-представление: {delta_number}")

    # дельта-декодирование
    for number in [344431, 871, 324, 141]:
        delta_decoded_number = coder.delta_decoding(coder.delta_encoding(number))
        logger.info(f"Число {number}, дельта-декодированное число: {delta_decoded_number}")

    # индекс до сжатия
    index_test_orig = index_test.get_index()

    logger.info(f"До сжатия размер в КБ: {asizeof.asizeof(index_test_orig) / 1024}")
    for i, key in enumerate(index_test_orig.keys()):
        if i == 3: break
        logger.info(f"{key} : {index_test_orig[key]}")

    index_test.compress_index(method="gamma")

    # индекс после сжатия
    index_test_gamma = index_test.get_index()
    logger.info(f"После gamma-сжатия размер в КБ:{asizeof.asizeof(index_test_gamma) / 1024}")
    for i, key in enumerate(index_test_gamma.keys()):
        if i == 3: break
        logger.info(f"{key} : {index_test_gamma[key]}")

    coder = EliasCoder()
    b = bitarray(coder.gamma_encoding(15))
    logger.info(b)
    logger.info(bitarray("0001111"))

    logger.info(b.to01())


if __name__ == "__main__":
    start()
