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

    def setSourceLanguage(self):
        print("Type the number of your language:")
        self.sourceLanguage = int(input()) - 1

    def setTargetLanguage(self):
        print("Type the number of language you want to translate to:")
        self.targetLanguage = int(input()) - 1

    def output_language(self):
        for i, language in enumerate(languages):
            print(f"{i+1}. {language}")

    def get_url(self, word: str):
        translation = f"{languages[self.sourceLanguage].lower()}-{languages[self.targetLanguage].lower()}"
        return f"https://context.reverso.net/translation/{translation}/{word}"

    def print_title_word(self):
        print(f"{languages[self.targetLanguage]} Translations:")

    def print_title_phrase(self):
        print(f"{languages[self.targetLanguage]} Examples:")

if __name__ == '__main__':
    l = Language()
    print('Hello, welcome to the translator. Translator supports:')
    l.output_language()
    l.setSourceLanguage()
    l.setTargetLanguage()

    print('Type the word you want to translate:')
    word = input()

    url = l.get_url(word)
    headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}
    user_agent = 'Mozilla/5.0'
    user_agent2 = 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'
#    print(url)
    result = requests.get(url, headers={'User-Agent': user_agent2})
#    print(result.status_code)
    if result.status_code == 200:
        soup = BeautifulSoup(result.text, 'html.parser')

        trans_tags = soup.find_all('a', class_ = 'translation ltr dict n')
        trans_words = [word.get_text().strip() for word in trans_tags if word.get_text().strip() != '']

        phrase_source_tags = soup.find_all('div', class_ = 'src ltr')
        phrase_target_tags = soup.find_all('div', class_ = 'trg ltr')
        phrase_source_trans = [phrase.get_text().strip() for phrase in phrase_source_tags]
        phrase_target_trans = [phrase.get_text().strip() for phrase in phrase_target_tags]

        l.print_title_word()
        for word in trans_words:
            print(word)

        print()

        l.print_title_phrase()
        for source, target in zip(phrase_source_trans, phrase_target_trans):
            print(source)
            print(target)
            print()

    else:
        print("Connection error occurred while connecting to the context.reverso.net")
