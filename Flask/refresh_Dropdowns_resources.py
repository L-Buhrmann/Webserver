import pyodbc
import pandas as pd
import warnings


#Die Funktion gibt die in der Datenbank vorhandenen Productnummern und Resourcennummern als Liste wieder, um Dropdown-Menüs zu füllen

def refresh_resources():

    warnings.filterwarnings('ignore')
    server = 'tcp:cloud4automationserver.database.windows.net' 
    database = 'Cloud4AutomationDB'
    username = 'cloud4automationadmin' 
    password = 'keyword1!'
    driver = '{ODBC Driver 17 for SQL Server}'



    connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:clouddatasps.database.windows.net;DATABASE=SpeicherCloud;UID=Laurits;PWD=YouShallNotPass!"

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
  
    Products = readAnyTable("Product")
    products = []
    for x in Products[''].values :
        products.append(x)
    Resources = readAnyTable("Resource")
    resources = []
    for x in Resources['ResourceID'].values :
        resources.append(x)
    resources = list(dict.fromkeys(resources))
    return resources , products