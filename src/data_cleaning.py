import os
import sys
module_path = os.path.abspath(os.path.join(os.pardir))
if module_path not in sys.path:
    sys.path.append(module_path)
    
import numpy as np
import pandas as pd
import datetime

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


def sales_2019(df_in):
    df = df_in
    df = df[df['DocumentDate'].str.contains('2019') == True]
    return df