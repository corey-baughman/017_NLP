# 017 prepare.py
#=================================================

    # imports:
    
# general imports
import numpy as np
import pandas as pd

# text and file handling
import unicodedata
import re
import json
import os

# NLP
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
#=================================================

    # functions:
    
def basic_clean(string):
    '''
    This function takes in a block of text and does some basic cleaning on it to include: 
        - lowering case of all letters
        - normalizing unicode characters using NKFD
        - encoding to ASCII characters to get rid of non_standard characters
        - decoding back to UTF-8 characters to be readable to Python
        - using regex to get rid of all characters that are not letters, numbers or whitespace.
    Arguments: a string of text to be cleaned.
    
    Returns: cleaned text string.
        '''
    string = unicodedata.normalize('NFKD', string).encode(
    'ascii', 'ignore').decode('utf-8').lower()
    string = re.sub(r'[^a-zA-Z0-9\s]', '', string)
    
    return string


def tokenize(string):
    '''
    This function takes in a block of text (string) and tokenizes it.
    
    Arguments: a text string
    
    Returns: a tokenized text string
    '''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    string = tokenizer.tokenize(string, return_str=True)  
    
    return string


def stem(string):
    '''
    This function takes in a block of text (string) and splits it into a list of individual words. It then uses the stem function on each word and finally joins the words back into a stemmed string.
    
    Arguments: a text string
    
    Returns: a stemmed text string
    '''
    stemmer = nltk.porter.PorterStemmer()
    string = ' '.join([stemmer.stem(word) for word in string.split()])
    
    return string


def lemmatize(string):
    '''
    This function takes in a block of text (string) and splits it into a list of individual words. It then uses the lemmatize function on each noun and verb and finally joins the words back into a lemmatized string.
    
    Arguments: a text string
    
    Returns: a lemmatized text string
    '''
    lemmatizer = nltk.stem.WordNetLemmatizer()
    string = [lemmatizer.lemmatize(word, 'v') for word in string.split()]
    string = ' '.join([lemmatizer.lemmatize(word, 'n') for word in string])
    
    return string

ADDITIONAL_STOPWORDS = ['r', 'u', '2', 'ltgt']

def remove_stopwords(string):
    '''
    This function takes in a block of text (string) and splits it into a list of individual words. It then checks to see if each word is in the stopwords list and rejoins all of the words that are not in the list.
    
    Arguments: a text string
    
    Returns: a lemmatized text string
    '''
    stopwords = nltk.corpus.stopwords.words('english') + ADDITIONAL_STOPWORDS
    string = ' '.join([word for word in string.split() if word not in stopwords])
    
    return string


def make_comparative_df(df):
    '''
    This function takes in a dataframe of text entries and returns a 
    comparative dataframe with a column of the original entries and new
    columns "clean", "stemmed", and "lemmatized" with the original texts
    cleaned (see basic_clean() in this module, stemmed and lemmatized
    
    Arguments: a dataframe of texts
    
    Returns: a dataframe of the original texts and comparative columns
            of the various steps of cleaning and prepping for NLP analysis
    '''
    df.rename(columns={'content':'original'}, inplace=True)
    df['clean'] = df.original.apply(basic_clean).apply(tokenize).apply(
    remove_stopwords)
    df['stemmed'] = df.clean.apply(stem)
    df['lemmatized'] = df.clean.apply(lemmatize)
    
    return df

def prep_spam(df):
    '''
    Takes in spam df and cleans, tokenizes, lemmatizes.
    
    Arguments: spam df
    Returns: spam df with the text column
    cleaned, tokenized, and lemmatized.
    '''
    df = df.drop(columns='id')
    df.text = df.text.apply(basic_clean).apply(tokenize).apply(
    remove_stopwords)
    
    return df




def clean(text):
    '''
    A simple function to cleanup text data.
    '''
    wnl = nltk.stem.WordNetLemmatizer()
    stopwords = nltk.corpus.stopwords.words('english') + ADDITIONAL_STOPWORDS
    text = (unicodedata.normalize('NFKD', text)
             .encode('ascii', 'ignore')
             .decode('utf-8', 'ignore')
             .lower())
    words = re.sub(r'[^\w\s]', '', text).split()
    return [wnl.lemmatize(word) for word in words if word not in stopwords]
