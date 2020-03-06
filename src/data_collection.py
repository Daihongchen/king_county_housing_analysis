import numpy as np
import pandas as pd

import psycopg2


## this function created the datafiles for data clean
dbname = "king_house"

conn = psycopg2.connect(dbname = dbname)

def create_df_dict():
    df_sale = pd.read_sql("""
                        SELECT * 
                        FROM extr_rpsale""", conn)
    
    df_rdb = pd.read_sql("""
            SELECT *
            FROM extr_resbldg
            """, conn)

    df_parcel = pd.read_sql("""
            SELECT *
            FROM extr_parcel
            """, conn)

    df_lookup = pd.read_sql("""
            SELECT *
            FROM look_up
            """, conn)

    df_dict = {'df_rdb': df_rdb, 
                'df_parcel': df_parcel, 
                'df_sale': df_sale, 
                'df_lookup': df_lookup}
                
    return df_dict
    
