import pandas as pd
import numpy as np
import os
# use get_db_url function to connect to the codeup db
from env import get_db_url

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
        SELECT bathroomcnt, bedroomcnt, calculatedfinishedsquarefeet, fips, latitude, longitude,
        propertylandusetypeid, regionidcounty, regionidzip, yearbuilt, taxvaluedollarcnt, taxamount, transactiondate
        FROM properties_2017
        JOIN predictions_2017 USING (parcelid)
        where transactiondate between "2017-05-01" and "2017-08-31";
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
    train, test = train_test_split(df, train_size=0.8, random_state=123)
    train, validate = train_test_split(train, train_size=0.7, random_state=123)
    return train, validate, test