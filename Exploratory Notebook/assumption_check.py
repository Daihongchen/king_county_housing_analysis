import numpy as np
import pandas as pd

import psycopg2
import datetime

import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.diagnostic import linear_rainbow, het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.preprocessing import LabelEncoder 


def correlation_fig(df):
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=np.bool))

    fig1, ax1 = plt.subplots(figsize=(11, 9))
    sns.heatmap(corr, mask=mask, ax=ax1)
    sns.pairplot(df)

    
def create_df(df, columns):
    return df[columns].copy()


def create_model(df):
    df.dropna(inplace=True)
    model = ols(formula="df.iloc[:, 0] ~ df.iloc[:, 1:]", data = df).fit()
    return model


def model_summary (model): 
    
    return model.summary()


def linearity_check(model):

    rainbow_statistic, rainbow_p_value = linear_rainbow(model)
    
    print("Rainbow statistic:", rainbow_statistic)
    print("Rainbow p-value:", rainbow_p_value)
    print("\n")
    print("The null hypothesis is that the model is linearly predicted by the features,\
alternative hypothesis is that it is not. Thus returning a low p-value means that the current model violates the linearity assumption.")


def normality_check():
    print(f"The Jarque-Bera test is performed automatically as part of the model summary output, labeled Jarque-Bera (JB) and Prob(JB).\
    \n\nThe null hypothesis is that the residuals are normally distributed, alternative hypothesis is that they are not. \
Thus returning a low p-value means that the current model violates the normality assumption.")

    
def homosdt_check_fig(df, model):
      
    y = df.iloc[:,0]
    y_hat = model.predict()
    fig2, ax2 = plt.subplots()
    ax2.set(xlabel=f"Predicted {df.columns[0]}",
            ylabel=f"Residuals (Actual - Predicted {df.columns[0]})")
    fig = ax2.scatter(x=y_hat, y=y-y_hat, color="blue", alpha=0.2)
    
    return fig


def homosdt_check_test(df, model):
    y = df.iloc[:,0]
    y_hat = model.predict()
    lm, lm_p_value, fvalue, f_p_value = het_breuschpagan(y-y_hat, df.iloc[:, 1:])
    print("Lagrange Multiplier p-value:", lm_p_value)
    print("F-statistic p-value:", f_p_value)
    print("\n")
    print("The null hypothesis is homoscedasticity, alternative hypothesis is heteroscedasticity.\
Thus returning a low p-value means that the current model violates the homoscedasticity assumption")

    
def independence_check(df):

    rows = df.iloc[:, 1:].values

    vif_df = pd.DataFrame()
    vif_df["VIF"] = [variance_inflation_factor(rows, i) for i in range(2)]
    vif_df["feature"] = df.columns[1:]

    vif_df