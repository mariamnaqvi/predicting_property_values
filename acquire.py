import pandas as pd
import numpy as np
import os
# use get_db_url function to connect to the codeup db
from env import get_db_url

import matplotlib.pyplot as plt

def get_zillow_data(cached=False):
    '''
    This function returns the zillow database as a pandas dataframe. 
    If the data is cached or the file exists in the directory, the function will read the data into a df and return it. 
    Otherwise, the function will read the database into a dataframe, cache it as a csv file
    and return the dataframe.
    '''
    # If the cached parameter is false, or the csv file is not on disk, read from the database into a dataframe
    if cached == False or os.path.isfile('telco_df.csv') == False:
        sql_query = '''
        SELECT parcelid, latitude, longitude, fips AS county, yearbuilt, bathroomcnt AS num_baths, bedroomcnt AS num_beds, calculatedfinishedsquarefeet AS num_sqft,
        propertylandusedesc AS property_desc, taxvaluedollarcnt AS tax_value
        FROM properties_2017
            JOIN predictions_2017 USING (parcelid)
        	JOIN propertylandusetype USING (propertylandusetypeid)
        WHERE transactiondate BETWEEN "2017-05-01" AND "2017-08-31"
            AND propertylandusetypeid IN (261, 263, 264, 265, 266, 268, 273, 275, 276, 279);
        '''
        zillow_df = pd.read_sql(sql_query, get_db_url('zillow'))
        #also cache the data we read from the db, to a file on disk
        zillow_df.to_csv('telco_df.csv')
    else:
        # either the cached parameter was true, or a file exists on disk. Read that into a df instead of going to the database
        zillow_df = pd.read_csv('zillow_df.csv', index_col=0)
    # return our dataframe regardless of its origin
    return zillow_df


def get_data_summary(df):
    '''
    This function takes in a pandas dataframe and prints out the shape of the dataframe, number of missing values, 
    columns and their data types, summary statistics of numeric columns in the dataframe, as well as the value counts for categorical variables.
    '''
    # Print out the "shape" of our dataframe - the rows and columns we have to work with
    print(f'The zillow dataframe has {df.shape[0]} rows and {df.shape[1]} columns.')
    print('')
    print('-------------------')

    # print the number of missing values in our dataframe
    print(f'There are total of {df.isna().sum().sum()} missing values in the entire dataframe.')
    print('')
    print('-------------------')

    # print some information regarding our dataframe
    df.info()
    print('')
    print('-------------------')
    
    # print out summary stats for our dataset
    print('Here are the summary statistics of our dataset')
    print(df.describe())
    print('')
    print('-------------------')

    print('Here are the categories and their relative proportions')
    # check different categories and proportions of each category for object type cols
    show_vc = ['county','num_baths','num_beds', 'property_desc']
    for col in df.columns:
        if col in show_vc:
            print(f'value counts of {col}')
            print(df[col].value_counts())
            print('')
            print(f'proportions of {col}')
            print(df[col].value_counts(normalize=True,dropna=False))
            print('-------------------')