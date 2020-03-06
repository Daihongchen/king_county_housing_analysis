import os
import sys
module_path = os.path.abspath(os.path.join(os.pardir))
if module_path not in sys.path:
    sys.path.append(module_path)
    
import numpy as np
import pandas as pd
import datetime

import statsmodels.api as sm
import statsmodels.stats.api as sms
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import linear_rainbow, het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor


# initiate dfs from csv files
def create_dfs(csv1, csv2, csv3, csv4):
    relative_filename = os.path.abspath(os.path.join(os.pardir, 'data', csv1))
    df1 = pd.read_csv(relative_filename)
    
    relative_filename = os.path.abspath(os.path.join(os.pardir, 'data', csv2))
    df2 = pd.read_csv(relative_filename)
    
    relative_filename = os.path.abspath(os.path.join(os.pardir, 'data', csv3))
    df3 = pd.read_csv(relative_filename, encoding='latin-1')
    
    relative_filename = os.path.abspath(os.path.join(os.pardir, 'data', csv4))
    df4 = pd.read_csv(relative_filename)
    
    return df1, df2, df3, df4


# create sales df that only includes sales from 2019
def sales_2019(df):
    df = df[df['DocumentDate'].str.contains('2019') == True]

    return df

# clean and prep sales df for joining and analysis
def clean_sales(df_in):
    df = df_in
    
    #remove all columns that are not relevant for analysis
    columns = ['Major', 'Minor', 'DocumentDate', 'SalePrice', 'PropertyType', 'HID']
    df = df[columns]
    
    #remove all rows with sale value of $0
    df = df[df['SalePrice'] > 0]
    
    return df

# clean and prep parcel df for joining and analysis
def clean_parcel(df_in):
    df = df_in
    
    #create new column for whether or not house is on waterfront property
    df['waterfront'] = (df['WfntLocation'] > 0).astype(int)
    
    # new column for whether or not there are power lines
    df['pwrlines'] = df['PowerLines'] == 'Y'

    # new column for whether or not there is some other nusiance
    df['othernuisance'] = df['OtherNuisances'] == 'Y'
    
    # new column for totalling all values from nuisance columns (booleans counted as 0 or 1)
    df['nuisance_total'] = (
        df['AirportNoise'] +
        df['TrafficNoise'] +
        df['pwrlines'] +
        df['othernuisance']
        )
    
    # new boolean column for whether or not property has any kind of nuisance present
    df['nuisance'] = (df['nuisance_total'] > 0).astype(int)
    
    return df

def clean_master(df_master):
    df_master = df_master[df_master['SalePrice'] > 50000]
    df_master = df_master[df_master['PropertyType'] == 11]
    
    return df_master

# add Major and Minor columns of the df to create HID column - used for joining tables
def add_hid(df_in):
    df = df_in
    df['HID'] = (df['Major'].astype(str)).str.zfill(6) + '-' + (df['Minor'].astype(str)).str.zfill(4)
    
    return df
    
# join all dataframes on the HID column
def join_dfs(df1, df2, df3):
    df_master = df1.merge(df2, how='inner', on='HID')
    df_master = df_master.merge(df3, how='inner', on='HID')
    
    return df_master

def create_model(dependent, features, df_master):
    
    desired_cols = dependent + features
    df_model = df_master[desired_cols].copy()
    df_model.dropna(inplace=True)

    y = df_model[dependent]
    x = df_model[features]

    model = sm.OLS(y, sm.add_constant(x)).fit()
    
    return df_model, model

def linearity_check(model):

    rainbow_statistic, rainbow_p_value = linear_rainbow(model)
    
    print("Rainbow statistic:", rainbow_statistic)
    print("Rainbow p-value:", rainbow_p_value)
    pass

def vif_test(df_model, features):
    
    rows = df_model[features].values

    vif_df = pd.DataFrame()
    vif_df["VIF"] = [variance_inflation_factor(rows, i) for i in range(len(features))]
    vif_df["feature"] = features

    return vif_df
