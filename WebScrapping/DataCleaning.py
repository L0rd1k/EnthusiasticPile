import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import re
import string

urls = ['https://learnenglish.britishcouncil.org/general-english/stories/a-serious-case',
        'https://learnenglish.britishcouncil.org/general-english/video-zone/black-british-history',
        'https://learnenglish.britishcouncil.org/general-english/video-zone/ten-cat-facts'
        ]

class SiteScrapper:
    article_title = list()
    article_text = list()
    articles = dict()

    def __init__(self, urls):
        self.urls = urls

    def getArticleTitle(self, soup):
        article_title = [p.text for p in soup.find(class_="title").find_all('h1')]
        return article_title

    def getArticleText(self,soup):
        article_text = [p.text for p in soup.find(class_="node-article").find_all('p')]
        return article_text

    def sitesDataToSoup(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, "lxml")
        r_title = self.getArticleTitle(soup)
        r_text = self.getArticleText(soup)
        dictionary = dict()
        for i, c in enumerate(r_title):
            dictionary.update({r_title[i]: r_text})
        return dictionary

    def getArticlePagesInfo(self):
        articles = [self.sitesDataToSoup(url) for url in self.urls]
        return articles


class UtilsFunction():
    def __init__(self):
        pass

    def clean_text_round1(self, text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text

    def textCombination(self, list_of_text):
        combined_text = ''.join(list_of_text)
        return combined_text


def main():
    scrapper = SiteScrapper(urls)
    articles = scrapper.getArticlePagesInfo()
    utils = UtilsFunction()

    try:
        os.mkdir("transcripts")
    except OSError:
        pass
    else:
        print("Successfully created the directory!")
    for key in articles:
        for ele in key:
            with open("transcripts/article_" + str(ele) + ".txt","w+") as file:
                file.writelines(key.get(ele))

    data = {}
    for key in articles:
        for ele in key:
            with open("transcripts/article_" + str(ele) + ".txt","r+") as file:
                data[ele] = key.get(ele)

    data_combined = {key: [utils.textCombination(value)] for (key,value) in data.items()}
    pd.set_option('max_colwidth', 150)
    data_df = pd.DataFrame.from_dict(data_combined).transpose()
    data_df.columns = ['Story']
    data_df = data_df.sort_index()
    print(data_df.head())


if __name__ == "__main__":
    main()

