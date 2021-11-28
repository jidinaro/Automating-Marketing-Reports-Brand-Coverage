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

To install Brand Coverage, just download Brand_Coverage.py and bc.py, and open with your edit IDLE to configure and execute it.

## Using Brand_Coverage.py

To use Brand_Coverage.py, follow these steps:

* Complete with your data, used on previous steps:
```python

import pandas as pd
import os
from bc import coverage
   
path = os.path.join(os.environ['USERPROFILE'])+r'\Desktop\Python\GitHub'  #set your path
```
* Here you read your clients portfolio, used as the base for the coverage, and the sales per client per product:
```python

client_db = pd.read_csv(os.path.abspath(os.path.join(path,'Input\Cartera.csv')),sep=",",header=0,error_bad_lines=False) #Check the file name
client_db['Cod Cli'] = client_db['Cod Cli'].astype(str) #Check the column name corresponding to client codes.
sales_db = pd.read_csv(os.path.abspath(os.path.join(path,'Input\Sales.csv')),sep=",",header=0) #Check the file name
sales_db['Cod Cli'] = sales_db['Cod Cli'].astype(str) #Check the column name corresponding to client codes.
skus = sales_db.SKU.unique().tolist() #Check the column name corresponding to SKUs or products. 
sales_db = sales_db.pivot(index="Cod Cli",columns="SKU",values="Vol Paq") #Check the column name corresponding to values. Also, sales data is supposed to be stacked. In case your data is unstacked, just skip this.
db_bc = pd.merge(client_db,sales_db,how='left',on='Cod Cli') #Check the column name corresponding to client codes.
```

* The next step is to define the dictionary of agg functions used on the pivot table. This is donde since it could be the case where all the columns do not use the same aggfunc.

```python
dic_agg = {}
for x in skus: dic_agg[x] = lambda x: (x>0).sum() #This function counts values greater than zero. 
dic_agg['Cod Cli'] = pd.Series.nunique #This function counts distinct values.
grouper = ['Region', 'Area', 'Zona'] #Specify your grouper for the pivot table.
```
* The last step is to execute the `coverage` function, in order to create the grouped pivot table per sku. Before executing the function, you would have to replace on `bc.py` the argument 'Cod Cli' (it appears 2 times) with the column name corresponding to your client codes.
```python
coverage(path, db_bc, grouper, skus, dic_agg)
```
* Compile and run the code. If fully run, then the script will export to your specified path, a formatted excel with the percentual coverage per grouper per sku.

## Contact
If you want to contact me you can reach me at juanidinaro@gmail.com.
