import pandas as pd
import numpy as np
import os
# use get_db_url function to connect to the codeup db
from env import get_db_url
# import to use in the split function
from sklearn.model_selection import train_test_split

def get_zillow_data(cached=False):
    '''
    This function returns the zillow database as a pandas dataframe. 
    If the data is cached or the file exists in the directory, the function will read the data into a df and return it. 
    Otherwise, the function will read the database into a dataframe, cache it as a csv file
    and return the dataframe.
    '''
    # If the cached parameter is false, or the csv file is not on disk, read from the database into a dataframe
    if cached == False or os.path.isfile('zillow_df.csv') == False:
        sql_query = '''
        SELECT bathroomcnt, bedroomcnt, calculatedfinishedsquarefeet,
        propertylandusetypeid, taxvaluedollarcnt
        FROM properties_2017
        JOIN predictions_2017 USING (parcelid)
        where transactiondate between "2017-05-01" and "2017-08-31"
        AND propertylandusetypeid in (261, 263, 264, 265, 266, 268, 273, 275, 276, 279);
        '''
        zillow_df = pd.read_sql(sql_query, get_db_url('zillow'))
        #also cache the data we read from the db, to a file on disk
        zillow_df.to_csv('zillow_df.csv')
    else:
        # either the cached parameter was true, or a file exists on disk. Read that into a df instead of going to the database
        zillow_df = pd.read_csv('zillow_df.csv', index_col=0)
    # return our dataframe regardless of its origin
    return zillow_df


def split_zillow(df):
    '''
    This function takes in a pandas dataframe, splits it into train, test and split dataframes and returns them.
    '''
    train, test = train_test_split(df, train_size=0.8, random_state=123)
    train, validate = train_test_split(train, train_size=0.7, random_state=123)
    return train, validate, test


def wrangle_zillow(df):
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
