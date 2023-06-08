import pyodbc
import pandas as pd
import warnings
from datetime import datetime

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
    print(query_result)
    return query_result , conn
Orders , conn = readAnyTable("Orders")
Orders1, conn1 = readAnyTable("AllPositions") 
if  Orders.empty:
        OrderID = 1
else :
        OrderID = Orders['OrderID'].values[-1] + 1
if(OrderID < Orders1['OrderID'].values[-1]): #OrderID < Orders1['OrderID'].values[-1]
        print(OrderID)
        print(Orders1['OrderID'].values[-1])
        OrderID = Orders1['OrderID'].values[-1] + 1