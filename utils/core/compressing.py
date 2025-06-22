import logging

logger = logging.getLogger(__name__)


class EliasCoder:
    def __init__(self):
        pass

    def gamma_encoding(self, number: int) -> str:
        """
        Функция для гамма-кодирования Элиаса

        Parameters
        ----------
        number : int
            число для кодирования
        """
        logger.debug("Запуск гамма кодирования")
        binary_repr = format(number, "b")
        n_of_bits = len(binary_repr)
        return "0" * (n_of_bits - 1) + binary_repr	# Префикс из нулей + бинарное число

    def gamma_decoding(self, encoded_number: str) -> int:
        """
        Функция для декодирования строки, закодированной с помощью гамма-кодирования Элиаса

        Parameters
        ----------
        encoded_number : str
            закодированное число
        """
        logger.debug("Запуск гамма декодирования")
        if encoded_number == "1":
            return 1
        else:
            prefix_length = encoded_number.index("1")
            return (2**prefix_length) + int(encoded_number[(prefix_length+1):], 2)
        
    def delta_encoding(self, number: int) -> str:
        """
        Функция для дельта-кодирования Элиаса

        Parameters
        ----------
        number : int
            число для кодирования
        """
        logger.debug("Запуск дельта кодирования")
        binary_repr_of_number = format(number, "b")
        n_of_bits_for_number = len(binary_repr_of_number)
        binary_repr_of_binary = format(n_of_bits_for_number, "b")
        n_of_bits_for_binary = len(binary_repr_of_binary)

        return "0" * (n_of_bits_for_binary - 1) + "1" + binary_repr_of_binary[1:] + binary_repr_of_number[1:]

    def delta_decoding(self, encoded_number: str) -> int:
        """
        Функция для декодирования строки, закодированной с помощью дельта-кодирования Элиаса

        Parameters
        ----------
        encoded_number : str
            закодированное число
        """
        logger.debug("Запуск дельта декодирования")
        if encoded_number == "1":
            return 1
        prefix_length = encoded_number.index("1")
        binary_repr_of_binary = encoded_number[(prefix_length+1) : (2*prefix_length+1)]
        n_of_bits_for_number = 2**prefix_length + int(binary_repr_of_binary, 2)
        return 2**(n_of_bits_for_number - 1) + int(encoded_number[-(n_of_bits_for_number-1):], 2)
    
    def decode_gamma_string(self, encoded_string: str):
        """
        Декодирование гамма кода Элиаса для строки, содержащей несколько чисел 

        Parameters
        ----------
        encoded_string : str
            Строка, содержащая закодированные гамма-алгоритмом Элиаса числа
        """
        logger.debug("Запуск гамма мульти-декодирования")
        decoded_result = []
        while encoded_string != "":
            length = encoded_string.index("1") + 1
            if length > 1:
                length = 2 * length - 1
                current_encoded_number = encoded_string[:length]
                encoded_string = encoded_string[length:]
            else:
                current_encoded_number = encoded_string[0]
                encoded_string = encoded_string[1:]

            decoded_result.append(self.gamma_decoding(current_encoded_number))

        return decoded_result

    def decode_delta_string(self, encoded_string: str):
        """
        Декодирование дельта кода Элиаса для строки, содержащей несколько чисел 
        
        Parameters
        ----------
        encoded_string : str
            Строка, содержащая закодированные дельта-алгоритмом Элиаса числа
        """
        logger.debug("Запуск дельта мульти-декодирования")
        decoded_result = []
        while encoded_string != "":
            m = encoded_string.index("1")
            if m > 0:
                l_part = encoded_string[m+1:2*m+1]
                l = 2**m + int(l_part, 2)
                k = l-1
                index = 2*m+1 + k
                current_encoded_number = encoded_string[:index]
                encoded_string = encoded_string[index:]  
            else:
                current_encoded_number = encoded_string[0]
                encoded_string = encoded_string[1:]                  

            decoded_result.append(self.delta_decoding(current_encoded_number))
        return decoded_result