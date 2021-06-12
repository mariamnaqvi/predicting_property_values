# cleaning the df
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# function to clean original df
def prep_zillow(df):
    # check for duplicates 
    num_dups = df.duplicated().sum()
    # if we found duplicate rows, we will remove them, log accordingly and proceed
    if num_dups > 0:
        print(f'There are {num_dups} duplicate rows in your dataset - these will be dropped.')
        print ('----------------')
        # remove the duplicates found
        df = df.drop_duplicates()

    else:
        # otherwise, we log that there are no dupes, and proceed with our process
        print(f'There are no duplicate rows in your dataset.')
        print('----------------')

    # check how many rows with null values
    null_rows = df.isnull().any(axis=1).sum()
    if null_rows > 0:
        print(f'There are {null_rows} rows with null values in your dataset - these will be dropped.')
        print ('----------------')
        # remove the null values found
        df = df.dropna()

    else:
        # otherwise, we log that there are no null values, and proceed with our process
        print(f'There are no rows with null values in your dataset.')
        print('----------------')

    #----------------------#
    #     Split Data       #
    #----------------------#

    # split data into train, validate, test dataframes by calling the split_zillow function
    train, validate, test = split_zillow(df, seed=123)

    # Now that we have our 3 dataframes, print their shapes and return them    
    train.info()

    print ('----------------')

    print(f'Shape of train split: {train.shape}')

    print ('----------------')

    print(f'Shape of test split: {validate.shape}')

    print ('----------------')

    print(f'Shape of validate split: {test.shape}')

    print ('----------------')
    
    return train, validate, test

def remove_outliers(df, cols, k):
    '''
    checks for outliers in original dataframe and removes all outliers not within IQR 
    '''
    for col in cols:
        q1, q3 = df[col].quantile([.25, .75])
        iqr = q3 - q1
        upper_bound = q3 + k * iqr
        lower_bound = q1 - k * iqr
        df = df[(df[col] < upper_bound) & (df[col] > lower_bound)]   
    return df

def split_zillow(df, seed=123):
    '''
    This function takes in a pandas dataframe and a random seed. It splits the original
    data into train, test and split dataframes and returns them.
    Test dataset is 20% of the original dataset
    Train is 56% (0.7 * 0.8 = .56) of the original dataset
    Validate is 24% (0.3 * 0.7 = 0.24) of the original dataset
    '''
    train, test = train_test_split(df, train_size=0.8, random_state=123)
    train, validate = train_test_split(train, train_size=0.7, random_state=123)
    return train, validate, test
