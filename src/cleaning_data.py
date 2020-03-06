import numpy as np
import pandas as pd

import os
import sys
module_path = os.path.abspath(os.path.join(os.pardir))
if module_path not in sys.path:
    sys.path.append(module_path)
import src.data_collection as dc 


def data_cleaned():

    df_dict = dc.create_df_dict()
    
    df_sale = df_dict['df_sale'] 

    df_rdb = df_dict['df_rdb']

    df_parcel = df_dict['df_parcel']

    df_rdb = df_rdb[df_rdb['Major'] != 'Major']
    df_rdb['HID'] = df_rdb['Major'].str.zfill(6) + '-'+ df_rdb['Minor'].str.zfill(4)

    df_parcel = df_parcel[df_parcel['Major'] != 'Major']
    df_parcel['HID'] = df_parcel['Major'].str.zfill(6) + '-' + df_parcel['Minor'].str.zfill(4)

    df_sale = df_sale[df_sale['Major'] != 'Major']
    df_sale['HID'] = df_sale['Major'].str.zfill(6) + '-' + df_sale['Minor'].str.zfill(4)
    df_sale_2019_set = df_sale[df_sale['DocumentDate'].str.contains('2019')]

    king_house_2019 = df_sale_2019_set.merge(df_parcel, how='inner', on='HID')
    king_house_2019 = king_house_2019.merge(df_rdb, how='inner', on='HID')

    king_house_2019 = king_house_2019.astype(
                     {'SalePrice':'float',
                      'SqFtLot':'float',  
                      'SqFt1stFloor':'float', 
                       'SqFtHalfFloor':'float',
                       'SqFt2ndFloor':'float', 
                       'SqFtUpperFloor':'float', 
                       'SqFtUnfinFull':'float', 
                       'SqFtUnfinHalf':'float',
                       'SqFtTotLiving':'float', 
                       'SqFtTotBasement':'float', 
                       'SqFtFinBasement':'float',
                       'FinBasementGrade':'float', 
                       'SqFtGarageBasement':'float', 
                       'SqFtGarageAttached':'float',
                       'SqFtOpenPorch':'float', 
                       'SqFtEnclosedPorch':'float', 
                       'SqFtDeck':'float',
                       'Bedrooms':'float', 
                       'BathHalfCount':'float', 
                       'Bath3qtrCount':'float', 
                       'BathFullCount':'float',
                       'TrafficNoise': 'int', 
                       '    AirportNoise':'float',
                       'LakeWashington': 'int'
                       }
                      )
    
    cols = list(king_house_2019.columns)
    cols = [cols[2]] + cols[:2] + cols[3:]
    king_house_2019 = king_house_2019[cols]
    king_house_2019 = king_house_2019[(
                                    (king_house_2019['PropertyType'] == '11') 
                                    |(king_house_2019['PropertyType'] == '12') 
                                    |(king_house_2019['PropertyType'] == '13') 
                                    |(king_house_2019['PropertyType'] == '14') 
                                    )
                                    & (king_house_2019.SalePrice >= 50000)]
    
    king_house_2019['SqlTotalGarage'] = king_house_2019['SqFtGarageBasement'] + king_house_2019['SqFtGarageAttached']

    king_house_2019['pwrlines'] = king_house_2019['PowerLines'] == 'Y'
    king_house_2019['othernuisance'] = king_house_2019['OtherNuisances']=='Y'

    king_house_2019['nuisance_total'] = (
                king_house_2019['AirportNoise'] +
                king_house_2019['TrafficNoise'] +
                king_house_2019['pwrlines'] +
                king_house_2019['othernuisance']
                )
    king_house_2019['nuisance_bool'] = (king_house_2019['nuisance_total'] > 0).astype('int')

    king_house_2019['is_waterfront'] = (king_house_2019['WfntLocation'] != '0').astype('int')

    king_house_2019['BathTotal'] = king_house_2019['BathHalfCount']*0.5 + king_house_2019['Bath3qtrCount'] * 0.75 + king_house_2019['BathFullCount']

    king_house_2019['PorchTotal'] = king_house_2019['SqFtOpenPorch'] + king_house_2019['SqFtEnclosedPorch']
    king_house_2019['is_porch'] = (king_house_2019['PorchTotal']!=0).astype('int')

    return king_house_2019