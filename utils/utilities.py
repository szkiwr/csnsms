import re

# URLの除外ワードを読み込む
def readExcludedWords(): 
    excluded_words = []
    with open('config/excluded_words.txt', 'r') as file:
        for line in file:
            word = line.strip()
            excluded_words.append(word)
    return excluded_words

# テキストからURLを抽出
def extractURLs(text):
    pattern = re.compile(r'(https?://\S+)')
    urls = re.findall(pattern, text)
    excluded_keywords = readExcludedWords()
    urls = set(filter(lambda x: all(keyword not in x for keyword in excluded_keywords), urls))
    urls = [re.sub(r'\).*$', '', x) for x in urls]
    return urls
