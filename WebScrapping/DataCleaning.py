import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import re
import string
from sklearn.feature_extraction.text import CountVectorizer


urls = ['https://learnenglish.britishcouncil.org/general-english/stories/a-serious-case',
        'https://learnenglish.britishcouncil.org/general-english/video-zone/black-british-history',
        'https://learnenglish.britishcouncil.org/general-english/video-zone/ten-cat-facts'
        ]

def initializer():
    try:
        os.mkdir("transcripts")
    except OSError:
        pass
    else:
        print("Successfully created the directory!")


class SiteScrapper:
    article_title = list()
    article_text = list()
    articles = dict()
    dictionary = dict()

    def __init__(self, urls):
        self.urls = urls

    def m_get_article_title(self, soup):
        article_title = [p.text for p in soup.find(class_="title").find_all('h1')]
        return article_title

    def m_get_article_text(self,soup):
        article_text = [p.text for p in soup.find(class_="node-article").find_all('p')]
        return article_text

    def m_sites_data_to_soup(self, url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, "lxml")
        r_title = self.m_get_article_title(soup)
        r_text = self.m_get_article_text(soup)
        for i, c in enumerate(r_title):
            self.dictionary.update({r_title[i]: r_text})
        return self.dictionary

    def m_get_article_pages_info(self):
        self.articles = [self.m_sites_data_to_soup(url) for url in self.urls]

    def m_save_articles_to_txt_file(self):
        for key in self.articles:
            for ele in key:
                with open("transcripts/article_" + str(ele) + ".txt", "w+") as file:
                    file.writelines(key.get(ele))


    def m_load_article_from_txt_file(self):
        data = {}
        for key in self.articles:
            for ele in key:
                with open("transcripts/article_" + str(ele) + ".txt","r+") as file:
                    data[ele] = key.get(ele)
        return data


class UtilsFunction():
    def __init__(self):
        pass

    def clean_text_round(self, text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text

    def clean_text_round_second(self, text):
        text = re.sub('[‘’“”…]', '', text)
        text = re.sub('\n', '', text)
        return text

    def textCombination(self, list_of_text):
        combined_text = ''.join(list_of_text)
        return combined_text


def main():
    initializer()
    scrapper = SiteScrapper(urls)
    scrapper.m_get_article_pages_info()
    scrapper.m_save_articles_to_txt_file()
    data = scrapper.m_load_article_from_txt_file()

    utils = UtilsFunction()

    data_combined = {key: [utils.textCombination(value)] for (key, value) in data.items()}
    pd.set_option('max_colwidth', 150)
    data_df = pd.DataFrame.from_dict(data_combined).transpose()
    data_df.columns = ['story']

    # CLEANING DATA 1
    text_round = lambda x: utils.clean_text_round(x)
    data_clean = pd.DataFrame(data_df.story.apply(text_round))

    # CLEANING DATA 2
    text_round2 = lambda x: utils.clean_text_round_second(x)
    data_clean2 = pd.DataFrame(data_clean.story.apply(text_round2))

    # Exclude common English stop words
    cv = CountVectorizer(stop_words="english")
    data_cv = cv.fit_transform(data_clean2.story)
    # Split text to single words
    data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_dtm.index = data_clean2.index
    data_dtm.to_pickle("dtm.pkl")
    data_clean2.to_pickle("data_clean.pkl")


    ###### LOAD DATA
    data = pd.read_pickle('dtm.pkl')
    data = data.transpose()
    #print(data.head())

    # Find the top 30 words said by each comedian
    top_article_words = {}
    for c in data.columns:
        top = data[c].sort_values(ascending=False).head(30)
        top_article_words[c] = list(zip(top.index, top.values))

    # Print the top 15 words said by each comedian
    for article, top_words in top_article_words.items():
        print(article)
        print(', '.join([word for word, count in top_words[0:14]]))
        print('---')



if __name__ == "__main__":
    main()

