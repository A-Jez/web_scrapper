from collections import Counter
from os import listdir
from string import punctuation
from matplotlib import pyplot as plt
import numpy as np


INPUT_FOLDER = 'articles_3'
MOST_COMMON_CNT = 20
PLOT_GRANUALITY = 10000

GRANUAL_CNT = {}
GLOBAL_CNT = Counter()

for index, file in enumerate(listdir(INPUT_FOLDER), start=1):
    file = open(f"{INPUT_FOLDER}/{file}", 'r', encoding='utf-8-sig')
    raw_article = file.read()
    article_words = ''.join(c for c in raw_article if c not in punctuation).lower().split()

    word_cnt = Counter(article_words)

    GLOBAL_CNT += word_cnt

    GRANUAL_CNT[str( (len(list(GLOBAL_CNT.elements())) // PLOT_GRANUALITY + 1) * PLOT_GRANUALITY )] = Counter(GLOBAL_CNT)
    file.close()



total_word_count = len(list(GLOBAL_CNT.elements()))
print(GLOBAL_CNT.most_common(20))
print(GRANUAL_CNT.keys())


def pieChart():
    labels = []
    sizes = []
    for keys, values in GLOBAL_CNT.most_common(MOST_COMMON_CNT):
        labels.append('{0} - {1:.2f} %'.format(keys, values/total_word_count*100))
        sizes.append(values)

    sizes.append(total_word_count)
    labels.append('others')

    plt.pie(sizes,  startangle=90, labeldistance=1.05, textprops={'fontsize': 15 })
    plt.legend(labels, loc=3)
    plt.axis('equal')
    plt.show()


def incrChart():
    y_pos = np.arange(len(GRANUAL_CNT.keys()))
    values = []
    labels = []
    print(y_pos)
    for ox, cnt in GRANUAL_CNT.items():
        labels.append(ox)
        unique = [k for k, v in cnt.items() if v == 1]
        values.append(len(unique))
    
    

    plt.bar(y_pos, values, align='center', alpha=0.8)
    plt.xticks(y_pos, labels, rotation=30)
    plt.ylabel('unikatowe słowa w artykule')
    plt.xlabel('tyś kolejnych słów')
    plt.title('2')
    plt.show()


def wordsChart():
    y_pos = np.arange(MOST_COMMON_CNT)
    values = []
    labels = []
    print(y_pos)
    for ox, cnt in GLOBAL_CNT.most_common(MOST_COMMON_CNT):
        labels.append(ox)
        values.append((cnt / total_word_count) * 100)
    
    plt.bar(y_pos, values, align='center', alpha=0.8)
    plt.xticks(y_pos, labels)
    plt.ylabel('% Pokrycia tekstu')
    plt.xlabel('kolejne słowa od najwięcej występujących')
    plt.title('3')
    plt.show()

pieChart()
incrChart()
wordsChart()
