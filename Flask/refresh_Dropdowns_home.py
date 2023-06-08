import pyodbc
import pandas as pd
import warnings

#Die Funktion gibt die In der Datenbank vorhandenen ProduktNamen und CustomerIDs als Liste wieder, um Dropdown-Menüs zu füllen
def refresh():

    warnings.filterwarnings('ignore')
    server = 'tcp:cloud4automationserver.database.windows.net' 
    database = 'Cloud4AutomationDB'
    username = 'cloud4automationadmin' 
    password = 'keyword1!'
    driver = '{ODBC Driver 17 for SQL Server}'

    def readAnyTable(tablename):
        conn = pyodbc.connect('DRIVER=' + driver + 
                        ';SERVER=' + server + 
                        ';DATABASE=' + database + 
                        ';UID=' + username + 
                        ';PWD=' + password)
        query_result = pd.read_sql_query(
              ''' 
                  SELECT *
                  FROM [{0}].[dbo].[{1}]
              '''.format(database,tablename), conn)
        #print(query_result)
        return query_result
  
    Customers =readAnyTable("Customer")
    customers = []
    for x in Customers['CustomerID'].values :
        customers.append(x)
    Products = readAnyTable("Product")
    products = []
    for x in Products['ProductName'].values :
        products.append(x)

    return customers , products