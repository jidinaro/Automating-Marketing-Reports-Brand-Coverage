# Automating Marketing Reports: Brand Coverage
Brand Coverage allows `sales and data analysts` in the industry sector to automate one of the most common reports in marketing,  that is the coverage per product with different leveles of aggregation. 

This is the first code I've ever made, hopefully a member of a series of "Automating Marketing Reports", and I think that could be useful for other people.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed Python 3 or higher.
* [Pandas](https://pandas.pydata.org/docs/index.html) for Python. 
 ```
      pip install pandas
 ```
* [Numpy](https://numpy.org/) for Python. 
 ```
      pip install numpy
 ```
 or just get the [Anaconda](https://docs.continuum.io/anaconda/) package where Pandas and Numpy are already installed.
  * [Xlsxwriter](https://xlsxwriter.readthedocs.io/index.html) for Python, in order to export the formatted output in Excel. If you want, you could display it formatted in Jupyter Notebook using Styler.
 ```
      pip install xlsxwriter
 ```
 
 ## Installing Brand Coverage

To install Brand Coverage, just download Brand_Coverage.py and open with your edit IDLE to configure and execute it.

## Using Brand_Coverage.py

To use Brand_Coverage.py, follow these steps:

* Complete with your data, used on previous steps:
```python

import pandas as pd
import numpy as np
import xlsxwriter
import os
   
path = os.path.join(os.environ['USERPROFILE'])+r'\Desktop\Python\GitHub'  #set your path
```
* Here you read your clients portfolio, used as the base for the coverage, and the sales per client per product:
```python

client_db = pd.read_csv(os.path.abspath(os.path.join(path,'Input\Cartera.csv')),sep=",",header=0) 
client_db['Cod Cli'] = client_db['Cod Cli'].astype(str)
sales_db = pd.read_csv(os.path.abspath(os.path.join(path,'Input\Sales.csv')),sep=",",header=0)
sales_db['Cod Cli'] = sales_db['Cod Cli'].astype(str)
skus = sales_db.SKU.unique().tolist()
sales_db = sales_db.pivot(index="Cod Cli",columns="SKU",values="Vol Paq")
db_bc = pd.merge(client_db,sales_db,how='left',on='Cod Cli')
```

* The next step is to create the pivot table of buyers, using the merged database between clients and sales:

```python

dic_agg = {}
for x in skus: dic_agg[x] = lambda x: (x>0).sum() 
dic_agg['Cod Cli'] = pd.Series.nunique
grouper = ['Region', 'Area', 'Zona']
pivot = pd.pivot_table(db_bc,index=grouper,aggfunc= dic_agg)
```

* Now, we can add subtotals to the Pivot Table and calculate the coverage for each SKU:

```python

pivot = pivot.reset_index()
pivot = pd.concat([
        pivot.assign(
            **{x: ' Total' for x in grouper[i:]}
        ).groupby(grouper).sum() for i in range(len(grouper)+1)
    ]).sort_index()
for j in pivot[skus]:
    pivot['COV - '+j] = pivot[j]/pivot['Cod Cli']    
```

* Optional Steps: Removing buyers and formatting the excel output
```python
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
```
* Compile and run the code. If fully run, then the script will export a formatted excel output with the percentual coverage per grouper per sku.

## Contact
If you want to contact me you can reach me at juanidinaro@gmail.com.
