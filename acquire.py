# 017 acquire.py
# ============================================================
   
    # imports:
    
# general imports
import numpy as np
import pandas as pd
import os
import re

# for webscraping
from requests import get
from bs4 import BeautifulSoup

# local modules
from env import user, host, password
# ============================================================

def get_connection(db, u=user, h=host, p=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    '''
    return f'mysql+pymysql://{u}:{p}@{h}/{db}'



def new_spam_data():
    '''
    This function queries the spam database from the CodeUp MySQL server. 
    
    Arguments: None
    
    Returns: DataFrame of properties queried
    '''
    sql_query = """
                select * from spam;
                """
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('spam_db'))
    
    return df


def get_spam_data():
    '''
    This function reads in curriculum_logs data from Codeup database, 
    writes data to a csv file if a local file does not exist, and 
    returns a df. Function relies on other functions in the wrangle.py module.
    '''
    if os.path.isfile('spam.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('spam.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_spam_data()
        
        # Cache data
        df.to_csv('spam.csv')
        
    return df


    # functions for CodeUp blog
    
def get_article_text():
    """
    Retrieve and return the text content of an article from Codeup's website.

    If the article text is available locally, it is read from the 'article.txt' file.
    If the article text is not available locally, it is fetched from the Codeup website and saved to 'article.txt' for future use.

    Arguments: None
    
    Returns:
        str: The text content of the article.
    """

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


def get_blog_articles_data(refresh=False):
    '''
    This function looks for a local file 'blog_articles.csv'
    unless the keyword argument 'refresh' is set to True. If 
    the file is found, it is returned as a dataframe. If the 
    file is not found or refresh is True, the function uses
    beautiful soup 4 to scrape the blog articles from 
    codeup.com/blogs and appends each article's content and 
    title as a dictionary in a list of dicts. The final
    list is written as 'blog_articles.csv' to the current
    directory and returned as a dataframe of blog articles
    and their titles.
    
    Arguments: Refresh=False or True to indicate if you 
    would like any existing blog_articles.csv file to be
    updated.
    '''
    
    if not os.path.isfile('blog_articles.csv') or refresh:
        
        url = 'https://codeup.com/blog/'
        headers = {'User-Agent': 'Codeup Data Science'}
        response = get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        links = [link['href'] for link in soup.select('h2 a[href]')]

        articles = []

        for url in links:

            url_response = get(url, headers=headers)
            soup = BeautifulSoup(url_response.text, 'html.parser')

            title = soup.find('h1', class_='entry-title').text
            content = soup.find('div', class_='entry-content').text.strip()
            compiled = re.compile(re.escape(title), re.IGNORECASE)
            content = compiled.sub('', content)

            article_dict = {
                'title': title,
                'content': content
            }

            articles.append(article_dict)
        
        blog_article_df = pd.DataFrame(articles)
        
        blog_article_df.to_csv('blog_articles.csv', index=False)
        
    return pd.read_csv('blog_articles.csv')



def get_news_articles_data(refresh=False):
    '''
    This function looks for a local file 'news_articles.csv'
    unless the keyword argument 'refresh' is set to True. If 
    the file is found, it is returned as a dataframe. If the 
    file is not found or refresh is True, the function uses
    beautiful soup 4 to scrape the news articles from 
    'https://inshorts.com/en/read' and appends each 
    article's content and title as a dictionary in a list of
    dicts. The final list is written as 'news_articles.csv' 
    to the current directory and returned as a dataframe of
    articles and their titles.
    
    Arguments: Refresh=False or True to indicate if you 
    would like any existing news_articles.csv file to be
    updated.
    '''
    
    if not os.path.isfile('news_articles.csv') or refresh:
        
        url = 'https://inshorts.com/en/read'
        response = get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        categories = [li.text.lower() for li in soup.select('li')][1:]
        categories[0] = 'national'

        inshorts = []

        for category in categories:

            cat_url = url + '/' + category
            response = get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            titles = [span.text for span in soup.find_all('span', itemprop='headline')]
            contents = [div.text for div in soup.find_all('div', itemprop='articleBody')]

            for i in range(len(titles)):

                article = {
                    'title': titles[i],
                    'content': contents[i],
                    'category': category,
                }

                inshorts.append(article)
                
        inshorts_article_df = pd.DataFrame(inshorts)
        
        inshorts_article_df.to_csv('news_articles.csv', index=False)
                
    return pd.read_csv('news_articles.csv')