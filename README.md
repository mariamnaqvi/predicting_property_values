Regression Project - Predicting Tax Values for Properties in 2017

Project Description

I used data from Zillow to find good predictors of tax values and create a Linear Regression Model. Perfomed data cleaning, wrangling and exploraton before moving to modeling.

Project Goals

1. Create scripts to perform the following:

- acquisition of data
- preparation of data
- exploration of data

2. Perform statistical analysis to test hypotheses

3. Build and evaluate Regression models to predict tax values for single unit properties

Business Goals

Initial Hypotheses
*Hypotheses 1:* I accepted/rejected the null hypotheses; Mean monthly charges of customers who churned are higher
* Confidence level = 0.99
* Alpha = 1 - Confidence level = 0.01
* H<sub>0</sub>: Mean monthly charges of customers who churned = Mean monthly charges of all customers
* H<sub>1</sub>: Mean monthly charges of customers who churned > Mean monthly charges of all customers

Data Dictionary
<<<<<<< Updated upstream
Name | Datatype | Definition | Possible Values 
--- | --- | --- | --- 
parcelid|non-null  int64|Unique identifier for each property|Numeric value
latitude|non-null  float64|angular distance north/south of the equator, for locating a property|Numeric value
longitude|non-null  float64|angular distance east/west of the meridian, for locating a property|Numeric value
county|non-null  float64| 4-digit county code|6037, 6059 or 6111
yearbuilt|non-null  float64| the year the property was constructed, in four digit form|4-digit Numeric value
num_baths|non-null  float64| number of baths available in the property|Numeric value
num_beds|non-null  float64| number of bedrooms available in the property|Numeric value
num_sqft|non-null  float64| the area/size of the property in feet, squared|Numeric value
property_desc|non-null  object| indicates the type of this property|Single Family Residential, Condominium, Cluster Home, Manufactured, Modular, Prefabricated Homes, Mobile Home, Townhouse
tax_value|non-null  float64| assessed tax value for this property|Numeric value

Additionally, a set of features were added to the data set:
Name | Datatype | Definition | Possible Values 
--- | --- | --- | --- 
county_6037|TYPE|encoded representation of whether or not the property is in the 6037 county code|0 = No, 1 = Yes
county_6059|TYPE|encoded representation of whether or not the property is in the 6059 county code|0 = No, 1 = Yes
county_6111|TYPE|encoded representation of whether or not the property is in the 6111 county code|0 = No, 1 = Yes
property_type| int64|indicates the type of this property, using the numbers 0-5| 0 = Single Family Residential, 1 = Condominium, 2= Cluster Home, 3 = Manufactured, Modular, Prefabricated Homes, 4 = Mobile Home, 5 = Townhouse
age_of_home|int64|represents the current age, in years, of the property|Numeric value
=======
age_of_home = 2021 - year built
Features Selection 
- fullbathcnt and calculated bathnbr each have over 117,000 null values vs bathroomcnt with about 2900 nulls so bathroom count was chosen
-  year built has a lot of nulls but if it has strong correlation to predictor we can keep it
- bedroomcnt is missing about the same values as bathroomcnt and the least number so those two will be kept
- treating age, fips, bathroom and bedroom count as discrete categorical variables 
- renamed columns in sql during acquisition
>>>>>>> Stashed changes

Project Planning

The overall process followed in this project, is as follows:

1. Plan
2. Acquire
3. Prepare
4. Explore
5. Model
6. Deliver

### 1. Plan
* create a list of tasks to complete in the Trello board
* Perform preliminary examination of the dataset
* Collect database details (connection information and credentials)

### 2. Acquire
* This is accomplished via the python script named “acquire.py”. The script will use credentials (stored in env.py) to collects data using a SQL query from the following tables:
1. properties_2017
2. predictions_2017 
3. propertylandusetype 
* Once data is collected from the above tables, it is stored in a CSV (Comma Separated Value) file on-disk; subsequent acquire.py calls will make use of this cached data rather than repeatedly accessing the database
* Finally, the get_data_summary() function will present a number of data-set metadata, including the following:
  * The number of rows/columns in the data set
  * The number of missing values
  * Basic information about the data
  * Summarty stats for the data
  * Listings of each category and relative proportions

### 3. Prepare
* This functionality is stored in the python script "prepare.py". It will perform the following actions:
1. Check for duplicate rows in the data set. If duplicates are detected, they are removed and appropriate log messages are returned
2. Check for null in the data set. If nulls are detected, they are dropped and appropriate log messages are returned
3. Encode property_type to a numeric value (it was previously a string/object) for analysis
4. Create an age_of_home feature, which will subtract property's yearbuilt property from the current year
5. One-hot encode the county to a trio of columns, each representing one of the three counties
6. Split the data into 3 datasets - train/test/validate - used in modeling

### 4. Explore
* This functionality resides in the "explore.py" file, which provides the following functionality:
  1. perform univariate analysis, by generating bar plot and box plots of certain variables and their distributions
  2. perform bivariate analysis
  3. perform multivariate analysis
* the above also demonstrates the need for further cleanup
  * Certain properties are listed as having 0 bedrooms *and* 0 bathrooms - these records must be incorrect and will be dropped in the notebook
  * there are a number of null values in the num_sqft column. These are addressed in the notebook by finding the mean square-footage for properties matching the bed/bathroom count of the records missing data, and inserting those averages in-place of the NaN values. The following property types were addressed:
    * Condominium properties with 2 bedrooms and 2 bathrooms
    * Single Family Residential properties with 5 bedrooms and 4.5 bathrooms
    * Single Family Residential properties with 1 bedroom and 1 bathroom
  * there are 27 records lacking a yearbuilt property - these will be substituted with the median value for this column, 1971


### 5. Model


### 6. Deliver

