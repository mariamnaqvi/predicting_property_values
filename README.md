# Regression Project - Predicting Tax Values for Properties in 2017

## Project Description

Perform statistical analysis on a Zillow dataset to drive the creation of an accurate model to predict property tax values. Perfomed data cleaning, wrangling and exploraton before moving to modeling.

## Project Goals

1. Create scripts to perform the following:
 - acquisition of data
 - preparation of data
 - exploration of data

2. Perform statistical analysis to test hypotheses

3. Build and evaluate Regression models to predict tax values for single unit properties

4. A separate goal: provide a distribution of tax rates for each geographical division (counties)

## Business Goals

* Discover drivers of property values. 
* Perform modeling, analysis and testing to verify the performance of a prediction model using linear regression.

## Initial Hypotheses
*Hypotheses 1:* I rejected the null hypotheses; Mean tax value of properties in county 6059 are higher than the overall average tax value
* Confidence level = 0.99
* Alpha = 1 - Confidence level = 0.01
* H<sub>0</sub>: Mean tax value of properties in county 6059 = Mean tax value of all properties
* H<sub>1</sub>: Mean tax value of properties in county 6059 > Mean tax value of all properties

*Hypotheses 2:* I rejected the null hypotheses; There is a linear correlation between age of property and tax value
* Confidence level = 0.99
* Alpha = 1 - Confidence level = 0.01
* H<sub>0</sub>: There is no linear correlation between age of property and tax value
* H<sub>1</sub>: There is a linear correlation between age of property and tax value

## Data Dictionary
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
county_6037|uint8|encoded representation of whether or not the property is in the 6037 county code|0 = No, 1 = Yes
county_6059|uint8|encoded representation of whether or not the property is in the 6059 county code|0 = No, 1 = Yes
county_6111|uint8|encoded representation of whether or not the property is in the 6111 county code|0 = No, 1 = Yes
property_type| int64|indicates the type of this property, using the numbers 0-5| 0 = Single Family Residential, 1 = Condominium, 2= Cluster Home, 3 = Manufactured, Modular, Prefabricated Homes, 4 = Mobile Home, 5 = Townhouse
age_of_home|int64|represents the current age, in years, of the property|Numeric value, basically 2021 - year built

## Project Planning

The overall process followed in this project, is as follows:

1. Plan
2. Acquire
3. Prepare
4. Explore
5. Model
6. Deliver

### 1. Plan
* Create a list of tasks to complete in the <a href="https://trello.com/b/XeGPl5ac/regression-project">Trello Board</a>
* Perform preliminary examination of the dataset
* Collect database details (connection information and credentials)

### 2. Acquire
* This is accomplished via the python script named “acquire.py”. The script will use credentials (stored in env.py) to collects data using a SQL query from the following tables:
	1. properties_2017
	2. predictions_2017 
	3. propertylandusetype
	* Additionally, the SQL query was used to only acquire single-unit properties with a transaction date in the hot months - as per the project criteria:
		*  Single-unit properties are defined as "a housing unit within a larger structure that can be used by an individual or household to eat, sleep, and live. The unit can be in any type of residence, such as a house, apartment, or mobile home, and may also be a single unit in a group of rooms"

### Columns Selected from the Original Data 
- fullbathcnt and calculated bathnbr each have over 117,000 null values; on the other hand, bathroomcnt contains approximately 2900 null values. Since this results in fewer data replacements, bathroomcnt was selected to represent the number of bathrooms in a property
 - A similar arguement can be made for bedroomcnt - since it has the fewest number of null values, it will be used to represent the number of bedrooms
- Similarly, the yearbuilt column contains a large number of nulls. However, if that category presents a strong correlation to predictor, it may be valuable to retain 
- Certain columns were renamed via sql during acquisition; these serve to maintain consistency and increase clarity among variable names

* Once data is collected from the above tables, it is stored in a CSV (Comma Separated Value) file on-disk; subsequent acquire.py calls will make use of this cached data rather than repeatedly accessing the database
* Finally, the get_data_summary() function will present a number of data-set metadata, including the following:
  * The number of rows/columns in the data set
  * The number of missing values
  * Basic information about the data
  * Summary stats for the data and value counts
  * Listings of each category and relative proportions

### 3. Prepare
* This functionality is stored in the python script "prepare.py". It will perform the following actions:
1. Examine individual distributions of data and identify outliers
* perform univariate analysis, by generating bar plots for each categorical variable, as well as box plots and histograms for quantitative variables
3. Check for duplicate rows in the data set. If duplicates are detected, they are removed and appropriate log messages are returned
4. Check for nulls in the data set - several such cases were identified and addressed as follows:
	* Certain properties are listed as having 0 bedrooms *and* 0 bathrooms - these records must be incorrect and will be dropped in the notebook
	* There are a number of null values in the num_sqft column. These are addressed in the notebook by finding the mean square-footage for properties matching the bed/bathroom count of the records missing data, and inserting those averages in-place of the NaN values. The following property types were addressed:
	    * Condominium properties with 2 bedrooms and 2 bathrooms
	    * Single Family Residential properties with 5 bedrooms and 4.5 bathrooms
	    * Single Family Residential properties with 1 bedroom and 1 bathroom
	* There are 27 records lacking a yearbuilt property - these will be substituted with the median yearbuilt using the imputer function
		* The median was used as it is more resistant to outliers than the mean 
5. Encode property_type to a numeric value (it was previously a string/object) for analysis
6. Create an age_of_home feature, which will subtract property's yearbuilt property from the current year
7. One-hot encode the county to a trio of columns, each representing one of the three counties
8. Attempt to remove the outliers using an IQR of 1.5 - although this did bring some distributions closer to normal, this reduced the correlation of predictors with the target variable. As a result, we proceeded without this process and instead made use of a Robust Scaler to reduce the effect of outliers.
	* Moreover, we opted not to remove outliers from the train split, as there would potentially be outliers in the validate/test sets. This could negatively impact the model's performance.
9. Split the data into 3 datasets - train/test/validate - used in modeling
	* Train: 56% of the data
	* Validate: 24% of the data
	* Test: 20% of the data

### 4. Explore
* This functionality resides in the "explore.py" file, which provides the following functionality:
  1. Perform bivariate analysis, by generating bar plots for categorical variables, as well as scatter plots for quantitative variables
  2. Perform multivariate analysis by generating scatter plots of each continuous variable against the target variable, by each categorical variable  
* Performed T-tests and correlation tests to test my initial hypotheses

### 5. Model
* Feature Selection:
	* Used Correlation (of predictors with the target variable) and RFE to select the top 5 features to include in the model
	* The following were selected:
		* 'latitude', 'longitude', 'num_beds', 'num_sqft', 'county_6111'
* Generate a baseline, against which all models will be evaluated
	* The baseline was calculated to have an RMSE of 620877.48; each of the models was evaluated against this baseline value
* Compare the models against the baseline and deduce which has the lowest RMSE and highest R-squared value
* Fit the best performing model on test data
* Create visualizations of the residuals and the actual vs predicted distributions

### 6. Deliver
* Present findings via PowerPoint slides

## To recreate
Simply clone the project locally and create an env.py file in the same folder as the cloned code. The format should be as follows:

```
host = ‘DB_HOST_IP’
user =  ‘USERNAME’
password = ‘PASSWORD’

def get_db_url(db, user=user, host=host, password=password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
```
    
In the above code, replace the `host`, `user` and `password` values with the correct Database Host IP address, Username and Password.

Next, open the Jupyter notebook titled “final_report_zillow” and execute the code within. 

## Takeaways
During the analysis process, I made use of the following regression models:
1. OLS Regression
2. Lasso + Lars
3. Tweedie Regressor GLM
4. Polynomial Regression

My results indicated that the Polynomial Regression model provided the highest R-squared of 44% and the lowest RMSE of 463791. This beat the baseline RMSE of 620877 and R-squared of -22%.

The square footage, location (latitude and longitude) and number of bedrooms were found to be the best drivers of tax value.

## Next Steps
If I had more time, I would:
* add more features to the models - garage, basement, pool
* explore other scaling methods
* collect more data related to higher-property values

