# NLP explore.py
#==========================================

    #imports

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
#==========================================

    #functions
    
def show_counts_and_ratios(df, column):
    """
    Takes in a dataframe and a string of a single column
    Returns a dataframe with absolute value counts and percentage value counts
    """
    labels = pd.concat([df[column].value_counts(),
                    df[column].value_counts(normalize=True)], axis=1)
    labels.columns = ['n', 'percent']
    labels
    return labels


def split_data(df, target=None):
    '''
    takes in a df and splits in into train, validate and test datasets. The percentage of the total rows assigned to each dataset is as follows: train = 56%, validate = 24%, test = 20%
    
    Arguments = a dataframe, target: the string literal of the target column name(defaults to none)
    
    Returns: three dataframes: train, test, and split'''
    train_validate, test = train_test_split(
        df, random_state = 9751, train_size = .7, stratify=df[target])
    train, validate = train_test_split(
        train_validate, random_state = 9751, train_size = .8, stratify=train_validate[target])
    
    return train, validate, test
