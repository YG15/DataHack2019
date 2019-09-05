# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 19:43:12 2019

@author: user
"""
#import pandas as pd
#df=pd.read_csv("C:\\Users\\user\\Google Drive\\Datahack 2019\\data\\Raw\\all_devices.csv")

def diff_list(li1, li2): 
    return (list(set(li1) - set(li2))) 

def get_categ_col_dummy (df):    
    numerical_columns = df.describe().columns
    categorical_cols=diff_list(df.columns,numerical_columns)
    print(categorical_cols)
    
    categorial = df[categorical_cols]
    #to prevent case-sensitive separation to different categories:
    categorial=categorial.apply(lambda x: x.str.lower(), axis=1)
    categorial_dummies = pd.get_dummies(categorial)
    df.drop(columns=categorical_cols, inplace=True)
    df=df.join(categorial_dummies)
    return df