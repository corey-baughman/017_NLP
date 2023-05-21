from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd
import re
from env import user, host, password


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


def get_blog_articles_data(refresh=False):
    
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