import sys

import requests
from bs4 import BeautifulSoup

languages = ["Arabic",
    "German",
    "English",
    "Spanish",
    "French",
    "Hebrew",
    "Japanese",
    "Dutch",
    "Polish",
    "Portuguese",
    "Romanian",
    "Russian",
    "Turkish",
]

class Language:
    def __init__(self):
        self.sourceLanguage = 0
        self.targetLanguage = 0
        self.translation = []
        self.phrase_source = []
        self.phrase_target = []


    def setSourceLanguage(self):
        print("Type the number of your language:")
        self.sourceLanguage = int(input()) - 1

    def setTargetLanguage(self):
        print("Type the number of a language you want to translate to or '0' to translate to all languages:")
        self.targetLanguage = int(input()) - 1

    def is_identical(self) -> bool:
        return self.sourceLanguage == self.targetLanguage

    def output_language(self):
        for i, language in enumerate(languages):
            print(f"{i+1}. {language}")

    def get_url(self, word: str):
        translation = f"{languages[self.sourceLanguage].lower()}-{languages[self.targetLanguage].lower()}"
        return f"https://context.reverso.net/translation/{translation}/{word}"

    def str_title_word(self) -> str:
        return f"{languages[self.targetLanguage]} Translations:"

    def print_title_word(self) -> str:
        print(self.str_title_word())

    def str_title_phrase(self) -> str:
        return f"{languages[self.targetLanguage]} Examples:"

    def print_title_phrase(self):
        print(self.str_title_phrase())


    def get_translation(self, word: str):
        url = self.get_url(word)
        user_agent = 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'
        result = requests.get(url, headers={'User-Agent': user_agent})
        if result.status_code != 200:
            raise Exception("Something wrong with your internet connection")
        soup = BeautifulSoup(result.text, 'html.parser')
        trans_tags = soup.find_all('a', class_ = 'translation ltr dict n')
        self.translation = [word.get_text().strip() for word in trans_tags if word.get_text().strip() != '']

        phrase_source_tags = soup.find_all('div', class_ = 'src ltr')
        phrase_target_tags = soup.find_all('div', class_ = 'trg ltr')
        self.phrase_source = [phrase.get_text().strip() for phrase in phrase_source_tags]
        self.phrase_target = [phrase.get_text().strip() for phrase in phrase_target_tags]

        if len(self.translation) == 0:
            raise Exception(f"Sorry, unable to find {word}")

        return self.translation, zip(self.phrase_source, self.phrase_target)

    def str_translation(self, cnt: int = 5) -> str:
        str = self.str_title_word() + "\n"
        for word in self.translation[:cnt]:
            str += word + "\n"
        return str

    def print_translation(self, cnt: int = 5):
        print(self.str_translation(cnt))

    def str_phrase(self, cnt: int = 5) -> str:
        str = self.str_title_phrase() + "\n"
        for source, target in zip(self.phrase_source[:cnt], self.phrase_target[:cnt]):
            str += source + "\n"
            str += target + "\n"
            str += "\n"
        return str

    def print_phrase(self, cnt: int = 5):
        print(self.str_phrase(cnt))

    def get_target_language_list(self):
        list = []
        if self.is_identical():
            return list
        if self.targetLanguage != -1:
            list.append(self.targetLanguage)
            return list

        for i, language in enumerate(languages):
            if i != self.sourceLanguage:
                list.append(i)

        return list

    def str_all(self, cnt: int = 5) -> str:
        str = self.str_translation(cnt) + "\n"
        str += self.str_phrase(cnt)
        return str

    def print_all(self, cnt: int = 5):
        print(self.str_all(cnt))

    def save_output(self, word, cnt: int = 5):
        lst = self.get_target_language_list()
        with open(word + '.txt', 'w', encoding='utf-8') as f:
            for i in lst:
                self.targetLanguage = i
                self.get_translation(word)
                f.write(self.str_all(cnt))

    def print_output(self, word: str, cnt: int = 5):
        lst = self.get_target_language_list()
        for i in lst:
            self.targetLanguage = i
            self.get_translation(word)
            self.print_all(cnt)

def get_language_index(language: str) -> int:
    for i, lang in enumerate(languages):
        if lang.lower() == language.lower():
            return i
    return -1

if __name__ == '__main__':

    l = Language()
    l.sourceLanguage = get_language_index(sys.argv[1])
    if l.sourceLanguage == -1:
        print(f"Sorry, the program doesn't support {sys.argv[1]}")
        exit(1)
    l.targetLanguage = get_language_index(sys.argv[2])
    if l.targetLanguage == -1:
        print(f"Sorry, the program doesn't support {sys.argv[2]}")
        exit(1)
    word = sys.argv[3]

#    print('Hello, welcome to the translator. Translator supports:')
#    l.output_language()
#    l.setSourceLanguage()
#    l.setTargetLanguage()

#    print('Type the word you want to translate:')
#    word = input()

#    l.get_translation(word)
    try:
        l.save_output(word, 1)
    except Exception as e:
        print(e)

#    l.print_output(word, 1)
