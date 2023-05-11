# 017 acquire.py
# ============================================================
   
    # imports:
    
# general imports
import numpy as np
import pandas as pd

# for webscraping
from requests import get
from bs4 import BeautifulSoup
# ============================================================

    # functions for CodeUp blog
    
def get_article_text():
    # if we already have the data, read it locally
    if path.exists('article.txt'):
        with open('article.txt') as f:
            return f.read()

    # otherwise go fetch the data
    url = 'https://codeup.com/data-science/math-in-data-science/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    article = soup.find('div', id='main-content')

    # save it for next time
    with open('article.txt', 'w') as f:
        f.write(article.text)

    return article.text


def get_list_of_blogs(url='https://codeup.com/blog/', headers={'User-Agent': 'Codeup Data Science'}):
    '''
    Retrieve list of blog post urls from codeup blog site.
    '''
    # use get from requests module to request webpage
    response = get(url, headers=headers)
    # use Beautiful Soup to parse the html in the response
    soup = BeautifulSoup(response.content, 'html.parser')
    # 
    
    
    