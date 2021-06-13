# cleaning the df
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import date

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


    # encode features

    # encode property_desc to change it from string to numeric to be used in the model
    df['property_type'] = df.property_desc.map({'Single Family Residential':0, 'Condominium':1, 'Cluster Home':2, 'Manufactured, Modular, Prefabricated Homes':3, 
    'Mobile Home':4, 'Townhouse':5})

    # encode yearbuilt as age of home
    df['age_of_home'] = (date.today().year - df.yearbuilt).astype(int)

    #----------------------#
    #  One hot encoding    #
    #----------------------#

    # encode categorical variable: county to numeric
    dummy_df=pd.get_dummies(df['county'], dummy_na=False, 
                            drop_first=False)

    # rename columns that have been one hot encoded
    dummy_df = dummy_df.rename(columns={6037.0: 'county_6037', 6059.0: 'county_6059', 6111.0: 'county_6111'})  

    # join dummy df to original df
    df = pd.concat([df, dummy_df], axis=1)

    # drop encoded columns
    # cols_to_drop = ['property_desc', 'county', 'yearbuilt']
    # df = df.drop(columns = cols_to_drop)
    # print(f'The following columns were encoded and dropped to limit redundancy: {cols_to_drop}')
    return df

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
    train, test = train_test_split(df, train_size=0.8, random_state=seed)
    train, validate = train_test_split(train, train_size=0.7, random_state=seed)

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

    