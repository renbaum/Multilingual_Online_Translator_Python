import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    print('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
    language = input()
    print('Type the word you want to translate:')
    word = input()
    print(f'You chose "{language}" as a language to translate "{word}".')

    translation = ""
    output_txt = ""
    output_phrase = ""

    match language:
        case "en":
            translation = "french-english"
            output_txt = "English Translations:"
            output_phrase = "English Examples:"
        case "fr":
            translation = "english-french"
            output_txt = "French Translations:"
            output_phrase = "French Examples:"

    url = f"https://context.reverso.net/translation/{translation}/{word}"
    headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}
    user_agent = 'Mozilla/5.0'
    user_agent2 = 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'
    result = requests.get(url, headers={'User-Agent': user_agent2})
    print(result.status_code)
    if result.status_code == 200:
        soup = BeautifulSoup(result.text, 'html.parser')

        trans_tags = soup.find_all('a', class_ = 'translation ltr dict n')
        trans_words = [word.get_text().strip() for word in trans_tags if word.get_text().strip() != '']

        phrase_source_tags = soup.find_all('div', class_ = 'src ltr')
        phrase_target_tags = soup.find_all('div', class_ = 'trg ltr')
        phrase_source_trans = [phrase.get_text().strip() for phrase in phrase_source_tags]
        phrase_target_trans = [phrase.get_text().strip() for phrase in phrase_target_tags]


        print(output_txt)
        for word in trans_words:
            print(word)

        print()

        print(output_phrase)
        for source, target in zip(phrase_source_trans, phrase_target_trans):
            print(source)
            print(target)
            print()

    else:
        print("Connection error occurred while connecting to the context.reverso.net")
