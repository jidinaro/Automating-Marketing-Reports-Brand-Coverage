import pandas as pd
import numpy as np
import xlsxwriter
import os
   
path = os.path.join(os.environ['USERPROFILE'])+r'\Desktop\Python\GitHub' 
client_db = pd.read_csv(os.path.abspath(os.path.join(path,'Input\Cartera.csv')),sep=",",header=0,error_bad_lines=False) 
client_db['Cod Cli'] = client_db['Cod Cli'].astype(str)
sales_db = pd.read_csv(os.path.abspath(os.path.join(path,'Input\Sales.csv')),sep=",",header=0)
sales_db['Cod Cli'] = sales_db['Cod Cli'].astype(str)
skus = sales_db.SKU.unique().tolist()
sales_db = sales_db.pivot(index="Cod Cli",columns="SKU",values="Vol Paq")
db_bc = pd.merge(client_db,sales_db,how='left',on='Cod Cli')
dic_agg = {}
for x in skus: dic_agg[x] = lambda x: (x>0).sum() 
dic_agg['Cod Cli'] = pd.Series.nunique
grouper = ['Region', 'Area', 'Zona']
pivot = pd.pivot_table(db_bc,index=grouper,aggfunc= dic_agg)
pivot = pivot.reset_index()
pivot = pd.concat([
        pivot.assign(
            **{x: ' Total' for x in grouper[i:]}
        ).groupby(grouper).sum() for i in range(len(grouper)+1)
    ]).sort_index()
for j in pivot[skus]:
    pivot['COV - '+j] = pivot[j]/pivot['Cod Cli']   
cov = ["COV - " + x for x in skus]
grouper.append('Cod Cli')
cov = cov+grouper
pivot.drop(columns=pivot.columns.difference(cov), inplace=True) 
pivot = pivot.reset_index()
rows = pivot.iloc[:,2] == ' Total'
rows =  [i+1 for i, x in enumerate(rows) if x]
group = pivot.iloc[:,2] != ' Total'
group =  [i+1 for i, x in enumerate(group) if x]
cov = [i for i, x in enumerate(pivot.columns.values) if x[:3] == 'COV']
writer = pd.ExcelWriter(os.path.abspath(os.path.join(path,'Output\Coverage.xlsx')),engine='xlsxwriter')
pivot.to_excel(writer,index=False,sheet_name='Summary', na_rep="")
wb = writer.book 
ws = writer.sheets['Summary']
num = wb.add_format({'num_format': '#,##0','align':'center'})
porc = wb.add_format({'num_format': '0%','align':'center'})
header_format = wb.add_format({'align':'center','valign':'top','text_wrap':True, 'bold':True,'bg_color':'#050978','font_color':'white'})
subtotal_num = wb.add_format({'bold':True,'bg_color':'#8b9dc3','num_format':'#,##0','align':'center','valign':'top'})
subtotal_porc = wb.add_format({'bold':True,'bg_color':'#8b9dc3','num_format':'0%','align':'center','valign':'top'})
ws.set_column(0,3,18,num)
for i in cov:
    ws.set_column(i,i,18,porc)
for col_num, value in enumerate(pivot.columns.values):
    ws.write(0, col_num, value, header_format)
ws.autofilter(0,0,len(pivot.index),len(pivot.columns)-1)
for i in rows:
    for j in range(0,4):
        ws.write(i,j, pivot.iloc[i-1,j],subtotal_num)
for i in rows:
    for j in range(4,len(pivot.columns)):
        ws.write(i,j, pivot.iloc[i-1,j],subtotal_porc)
for i in group:
   ws.set_row(i, None, None, {'level':1})
   
writer.save()
writer.close()