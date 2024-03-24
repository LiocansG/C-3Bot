import re
import string
import os


class Tokenizer:
    def __init__(self, language="english", exclude_stopwords=True):
        self.__language = language
        self.__stop_words = self.__load_stop_words()
        self.__exclude_stopwords = exclude_stopwords

    def tokenize_and_filter_sentence(self, sentence: str) -> list:
        sentence = self.__remove_punctuation(sentence)
        tokens = self.__tokenize(sentence)
        if (not self.__exclude_stopwords):
            tokens = self.__remove_stop_words(tokens)
        return tokens

    def __load_stop_words(self) -> set:
        stop_words = set()
        filename = os.path.abspath(f'../../ressources/stop_words/{self.__language}.txt')

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                stop_words.add(line.strip())
        return stop_words

    def __tokenize(self, sentence: str) -> list:
        pattern = r'\w+|\$[\d\.]+|\S+'
        tokens = re.findall(pattern, sentence.lower())
        return tokens

    def __remove_stop_words(self, tokens: list) -> list:
        filtered_words = [word for word in tokens if word not in self.__stop_words]
        return filtered_words

    def __remove_punctuation(self, sentence: str) -> str:
        translator = str.maketrans('', '', string.punctuation)
        return sentence.translate(translator)