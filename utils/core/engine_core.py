from nltk.tokenize import RegexpTokenizer
from pymorphy3 import MorphAnalyzer
from nltk.corpus import stopwords
from bitarray import bitarray
from utils.core.compressing import EliasCoder
import logging

logger = logging.getLogger(__name__)


class InvertedIndex:
    # Словарь индекса: токен → список ID документов
    def __init__(self):
        logger.debug("Построение индекса")
        self.index = {}
        self.documents = {}
        self.tokenizer = RegexpTokenizer(r'[а-яёa-z0-9]+')	# Токенизация
        self.stopwords_ru = stopwords.words("russian")		# Стоп-слова
        self.morph = MorphAnalyzer()				# Лемматизация
        self.compress_method = None				# Тип сжатия
        self.coder = EliasCoder()				# Класс кодирования

    def get_index(self):
        '''Возвращает текущий инвертированный индекс'''
        return self.index
    
    def insert_doc(self, document_id: int, text: str) -> None:
        '''
        Добавление документа и его токенов в индекс
        
        Parameters
        ----------
        document_id : int
            идентификатор документа
        text : str
            документ
        '''
        logger.debug("Вставляю документ")
        self.documents[document_id] = text
        
        # токенизация
        words = self._tokenize(text)
        # лемматизация и удаление стоп-слов
        words = self._lemmatize(words)
        
        self._update_index(document_id, words)

    def search(self, query: str) -> list[int]:
        '''
        Поиск документов в инвертированном индексе
        
        Parameters
        ----------
        query : str
            запрос в виде строки для поиска
        '''

        # токенизация
        words = self._tokenize(query)
        # лемматизация и удаление стоп-слов
        words = self._lemmatize(words)

        # Распаковка
        if self.compress_method == 'delta':
            logger.debug(f"Ищу строку {query} в дельта индексе")
            list_of_documents = self.coder.decode_delta_string(self.index[words[0]].to01())
        elif self.compress_method == 'gamma':
            logger.debug(f"Ищу строку {query} в гамма индексе")
            list_of_documents = self.coder.decode_gamma_string(self.index[words[0]].to01())
        else:
            logger.debug(f"Ищу строку {query}")
            list_of_documents = self.index[words[0]]
        
        # документы, содержащие первое слово запроса
        result_docs = set(doc_id for doc_id in list_of_documents)
        
        # пересекаем результаты для остальных слов запроса
        for word in words[1:]:
            if self.compress_method == 'delta':
                list_of_documents = self.coder.decode_delta_string(self.index[word].to01())
            elif self.compress_method == 'gamma':
                list_of_documents = self.coder.decode_gamma_string(self.index[word].to01())
            else:
                list_of_documents = self.index[word]

            result_docs &= set(doc_id for doc_id in list_of_documents)

        return list(result_docs)

    def get_doc(self, document_id: int) -> str:
        '''Возврат исходного документа по ID'''
        return self.documents.get(document_id)
    
    def compress_index(self, method: str) -> None:
        '''
        Сжатие данных за счет применения алгоритмов гамма и дельта кодирования Элиаса
        
        Parameters
        ----------
        method : str
            метод кодирования (gamma / delta)
        '''
        logger.debug(f"Сжимаю данные {method} методом")
        if method == 'gamma':
            for token in self.index.keys():
                compressed_documents_ids = bitarray("".join([self.coder.gamma_encoding(document_id) 
                                                             for document_id in self.index[token]]))
                self.index[token] = compressed_documents_ids
            self.compress_method = 'gamma'
        elif method == 'delta':
            for token in self.index.keys():
                compressed_documents_ids = bitarray("".join([self.coder.delta_encoding(document_id) 
                                                             for document_id in self.index[token]]))
                self.index[token] = compressed_documents_ids
            self.compress_method = 'delta'
        else:
            print('Параметр <method> указан неверно')
            return 
        
    def _update_index(self, document_id: int, words: list[str]) -> None:
        '''Обновление индекса: добавление токенов в список'''
        logger.debug("Обновляю индекс")
        for word in words:
            self.index.setdefault(word, []).append(document_id)

    def _tokenize(self, text: str) -> list[str]:
        '''Вспомогательный метод для выделения токенов с помощью tokenizer'''
        return self.tokenizer.tokenize(text.lower())
    
    def _lemmatize(self, tokens: list[str]) -> list[str]:
        '''Вспомогательный модуль для лемматизации токенов'''
        words = []
        for token in tokens:
            token_in_normal_form = self.morph.normal_forms(token)[0]
            if token_in_normal_form not in self.stopwords_ru:
                words.append(token_in_normal_form)
        return words
    