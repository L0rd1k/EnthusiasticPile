import requests
from bs4 import BeautifulSoup
import pickle
import os


def getArticleTitle(soup):
    title = [p.text for p in soup.find(class_="title").find_all('h1')]
    return title


def getArticleText(soup):
    a_text = [p.text for p in soup.find(class_="node-article").find_all('p')]
    return a_text


def sitesDataToTranscript(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    r_title = getArticleTitle(soup)
    r_text = getArticleText(soup)
    return r_title, r_text



urls = ['https://learnenglish.britishcouncil.org/general-english/stories/a-serious-case',
        'https://learnenglish.britishcouncil.org/general-english/video-zone/black-british-history',
        'https://learnenglish.britishcouncil.org/general-english/video-zone/ten-cat-facts'
        ]

articles = [sitesDataToTranscript(u) for u in urls]

try:
    os.mkdir("transcripts")
except OSError:
    print("Creation of the directory failed")
else:
    print("Successfully created the directory!")

for i, c in enumerate(articles):
    with open("transcripts/article_" + str(c[0]) + ".txt","w+") as file:
        file.writelines(articles[0][i])

        #pickle.dump(articles[i][1], file)

#
# data = {}
# for i, c in enumerate(transcripts):
#     with open("transcripts/article" + str(i) + ".txt", "rb") as file:
#         data[i] = pickle.load(file)
#
# print(data.keys())
# print(data[0])