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
   
path = os.path.join(os.environ['USERPROFILE'])+r'\Desktop\' #set your path
```
* Here you read your clients portfolio, used as the base for the coverage, and the sales per client per product.
```python

client_db = pd.read_csv(os.path.abspath(os.path.join(path,'Input\Cartera.csv')),sep=",",header=0) 
sales_db = pd.read_csv(os.path.abspath(os.path.join(path,'Input\Sales.txt')),sep=",",header=0)
sales_db = sales_db.pivot(index="Cod Cli",columns="SKU",values="Vol Paq")
db_bc = pd.merge(client_db,sales_db,how='left',on='Cod Cli')
```

* The next step is to create the pivot table of buyers, using de merged database between clients and sales bases.

```python

skus = sales_db.SKU.unique().tolist()
dic_agg = {}
for x in skus: dic_agg[x] = lambda x: (x>0).sum() 
dic_agg['Cod Cli'] = pd.Series.nunique
pivot = pd.pivot_table(db_bc,index=['Region',"Area","Zona"],aggfunc= dic_agg)
```

* Now, we can add subtotals to the Pivot Table and create the coverage value for each SKU.

```python

pivot = pivot.reset_index()
grouper = ['Region', 'Area', 'Zona']
pivot = pd.concat([
        pivot.assign(
            **{x: 'Total' for x in grouper[i:]}
        ).groupby(grouper).sum() for i in range(len(grouper)+1)
    ]).sort_index()
```
