import chardet
from chardet.universaldetector import UniversalDetector
import json

def encode_file(file):
    detector = UniversalDetector()
    with open(file, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result

def get_words_from_json(file_name, encode):
    words = []
    with open(file_name, 'r', encoding=encode['encoding']) as f:
        content = json.load(f)
    for line in content['rss']['channel']['items']:
        new_words = line['description'].lower().split()
        words += new_words
    return words

def get_words_longer_6_char(words):
    words_longer_6 = []
    for word in words:
        if len(word) > 6:
            words_longer_6.append(word)
    return words_longer_6

def get_sorted_words_rating(words):
    words_rating = []
    set_words = set(words)
    for word in set_words:
        words_rating.append([word, words.count(word)])
    words_rating = sorted(words_rating, key=lambda i: i[1], reverse=True)
    return words_rating

def print_top10(words_rating, file_name):
    if file_name == 'all files':
        print('\nТОП-10 слов из всех файлов новостей:')
    else:
        print('\nТОП-10 слов из файла новостей {}:' .format(file_name))
    for i in range(10):
        print('№{} "{}" - {}' .format(i+1, words_rating[i][0], words_rating[i][1]))

def home_work(files):
    all_words = []
    for file_name in files:
        encode = encode_file(file_name)
        words = get_words_longer_6_char(get_words_from_json(file_name, encode))
        words_rating = get_sorted_words_rating(words)
        print_top10(words_rating, file_name)
        all_words += words
    all_words = get_sorted_words_rating(all_words)
    print_top10(all_words, 'all files')

files = ["newsafr.json", "newscy.json", "newsfr.json", "newsit.json"]
home_work(files)