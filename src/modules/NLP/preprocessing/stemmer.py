# https://tartarus.org/martin/PorterStemmer/index.html

class Stemmer:

    def __init__(self):

        self.__vowels = [*"aeiou"]
        self.__consonants = [*"bcdfghjklmnpqrstwxz"]
        self.__step1a_suffixes = [("sses", "ss"), ("ies", "i"), ("ss", "ss"), ("s", "")]
        self.__step1b_suffixes = [("eed", "ee"), ("ed", ""), ("ing", "")]
        self.__step1_2b_suffixes = [("at", "ate"), ("bl", "ble"), ("iz", "ize")]
        self.__step1c_suffixes = [("y", "i")]
        self.__step2_suffixes = [
            ("ational", "ate"), ("tional", "tion"), ("enci", "ence"), ("anci", "ance"),
            ("izer", "ize"), ("bli", "ble"), ("alli", "al"), ("entli", "ent"), ("eli", "e"),
            ("ousli", "ous"), ("ization", "ize"), ("ation", "ate"), ("ator", "ate"), ("alism", "al"),
            ("iveness", "ive"), ("fulness", "ful"), ("ousness", "ous"), ("aliti", "al"), ("iviti", "ive"),
            ("biliti", "ble"), ("logi", "log")
        ]
        self.__step3_suffixes = [
            ("icate", "ic"), ("ative", ""), ("alize", "al"), ("iciti", "ic"), ("ical", "ic"),
            ("ful", ""), ("ness", "")
        ]
        self.__step4_suffixes = [
            ("al", ""), ("ance", ""), ("ence", ""), ("er", ""), ("ic", ""), ("able", ""),
            ("ible", ""), ("ant", ""), ("ement", ""), ("ment", ""), ("ent", ""), ("ou", ""),
            ("tion", "t"), ("sion", "s"), ("ism", ""), ("ate", ""), ("iti", ""), ("ous", ""),
            ("ive", ""), ("ize", "")
        ]

        self.__step5a_suffixes = [("e", "")]

        self.__step5b_suffixes = [("l", "")]

    def preprocess_text(self, tokens: list) -> list:
        stem_sentence = []
        for word in tokens:
            stem_sentence.append(self.__stem_word(word=word))
        return stem_sentence

    def __stem_word(self, word: str) -> str:
        stem = self.__step_1(word=word)
        stem = self.__step_2(word=stem)
        stem = self.__step_3(word=stem)
        stem = self.__step_4(word=stem)
        stem = self.__step_5(word=stem)
        return stem

    def __determine_class(self, char: str) -> str:
        if (char in self.__vowels):
            return "V"
        return "C"

    def __divide_into_class(self, word: str) -> list:
        classes = []
        for char in word:
            classfication = self.__determine_class(char=char)
            if len(classes) == 0 or classes[-1] != classfication:
                classes.append(classfication)
        return classes

    def __determine_m(self, word: str) -> int:
        classes = self.__divide_into_class(word=word)
        if len(classes) < 2:
            return 0
        if classes[0] == "C":
            classes = classes[1:]
        if classes[-1] == "V":
            classes = classes[:len(classes) - 1]
        m = len(classes) // 2 if (len(classes) / 2) >= 1 else 0
        return m

    # stem contains a vowel.
    def __contains_vowel(self, word: str) -> bool:
        if (len(word) > 1):
            for letter in word[1:-1]:
                if letter in self.__vowels:
                    return True
            return False

    # stem ends with a double consonant of any type.
    def __end_with_double_consonant(self, word: str) -> bool:
        if len(word) >= 2 and word[-1] in self.__consonants and word[-2] in self.__consonants:
            return True
        return False

    # stem ends with cvc (consonant followed by vowel followed by consonant)
    # where second consonant is not W, X or Y (see, weird y again!)
    def __end_with_cvc(self, word: str) -> bool:
        if (len(word) >= 3 and word[-3] in self.__consonants) and (word[-2] in self.__vowels) and (
                word[-1] in self.__consonants) and (word[-1] not in "wxy"):
            return True
        else:
            return False

    # Deal with Plurals and Past Participles
    def __step_1(self, word: str) -> str:
        stem = self.__step_1_a(word=word)
        stem = self.__step_1_b(word=stem)
        stem = self.__step_1_c(word=stem)
        return stem

    def __step_1_a(self, word: str) -> str:
        for suffix in self.__step1a_suffixes:
            if word.endswith(suffix[0]):
                return word[:-len(suffix[0])] + suffix[1]
        return word

    def __step_1_b(self, word: str) -> str:

        if (word.endswith(self.__step1b_suffixes[0][0]) and self.__determine_m(
                word=word[:-len(self.__step1b_suffixes[0][0])]) > 0):
            return word[:-len(self.__step1b_suffixes[0][0])] + self.__step1b_suffixes[0][1]

        if (word.endswith(self.__step1b_suffixes[1][0]) and self.__contains_vowel(
                word=word[:-len(self.__step1b_suffixes[1][0])])):
            return self.__step_1_2b(word[:-len(self.__step1b_suffixes[1][0])] + self.__step1b_suffixes[1][1])

        if (word.endswith(self.__step1b_suffixes[2][0]) and self.__contains_vowel(
                word=word[:-len(self.__step1b_suffixes[2][0])])):
            return self.__step_1_2b(word[:-len(self.__step1b_suffixes[2][0])] + self.__step1b_suffixes[2][1])

        return word

    def __step_1_2b(self, word: str) -> str:

        for suffix in self.__step1_2b_suffixes:
            if word.endswith(suffix[0]):
                return word[:-len(suffix[0])] + suffix[1]

        if (not word.endswith("s") and not word.endswith("z") and not word.endswith(
                "l") and self.__end_with_double_consonant(word=word)):
            return word[:-1]

        if (self.__determine_m(word=word) == 1 and self.__end_with_cvc(word=word)):
            return word + "e"

        return word

    def __step_1_c(self, word: str) -> str:
        for suffix in self.__step1c_suffixes:
            if (word.endswith(suffix[0]) and self.__contains_vowel(word=word[:-len(suffix[0])])):
                return word[:-len(suffix[0])] + suffix[1]
        return word

    def __step_2(self, word: str) -> str:
        for suffix in self.__step2_suffixes:
            if (word.endswith(suffix[0]) and self.__determine_m(word=word[:-len(suffix[0])]) > 0):
                return word[:-len(suffix[0])] + suffix[1]
        return word

    def __step_3(self, word: str) -> str:
        for suffix in self.__step3_suffixes:
            if (word.endswith(suffix[0]) and self.__determine_m(word=word[:-len(suffix[0])]) > 0):
                return word[:-len(suffix[0])] + suffix[1]
        return word

    def __step_4(self, word: str) -> str:
        for suffix in self.__step4_suffixes:
            if (word.endswith(suffix[0]) and self.__determine_m(word=word[:-len(suffix[0])]) > 1):
                return word[:-len(suffix[0])] + suffix[1]
        return word

    def __step_5(self, word: str) -> str:
        stem = self.__step_5_a(word=word)
        stem = self.__step_5_b(word=stem)
        return stem

    def __step_5_a(self, word: str) -> str:
        for suffix in self.__step5a_suffixes:
            if self.__determine_m(word=word[:-len(suffix[0])]) > 1 and word.endswith(suffix[0]):
                return word[:-len(suffix[0])] + suffix[1]

        for suffix in self.__step5a_suffixes:
            if (word.endswith(suffix[0]) and self.__determine_m(
                    word=word[:-len(suffix[0])]) == 1 and not self.__end_with_cvc(word=word[:-len(suffix[0])])):
                return word[:-len(suffix[0])] + suffix[1]

        return word

    def __step_5_b(self, word: str) -> str:
        for suffix in self.__step5b_suffixes:
            if (word.endswith(suffix[0]) and self.__determine_m(word=word) > 1 and self.__end_with_double_consonant(word=word)):
                return word[:-len(suffix[0])] + suffix[1]
        return word