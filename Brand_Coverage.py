# -*- coding: utf-8 -*-
"""
@author: Juan Ignacio Di Naro
"""

import pandas as pd
import os
from bc import coverage

path = os.path.join(os.environ['USERPROFILE'])+r'\Desktop\Python\GitHub' 
client_db = pd.read_csv(os.path.abspath(os.path.join(path,'Input\Cartera.csv')),sep=",",header=0,error_bad_lines=False) 
client_db['Cod Cli'] = client_db['Cod Cli'].astype(str)
sales_db = pd.read_csv(os.path.abspath(os.path.join(path,'Input\Sales.csv')),sep=",",header=0)
sales_db['Cod Cli'] = sales_db['Cod Cli'].astype(str)
skus = sales_db.SKU.unique().tolist()
sales_db = sales_db.pivot(index="Cod Cli",columns="SKU",values="Vol Paq")
db_bc = pd.merge(client_db,sales_db,how='left',on='Cod Cli')
grouper = ['Region', 'Area', 'Zona']
dic_agg = {}
for x in skus: dic_agg[x] = lambda x: (x>0).sum() 
dic_agg['Cod Cli'] = pd.Series.nunique
coverage(path, db_bc, grouper, skus, dic_agg)
