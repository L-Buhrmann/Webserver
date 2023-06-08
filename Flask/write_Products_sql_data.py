import pyodbc 

def writeDataIntoProducts(id,name) :
    server = 'tcp:cloud4automationserver.database.windows.net' 
    database = 'Cloud4AutomationDB'
    username = 'cloud4automationadmin' 
    password = 'keyword1!'
    driver = '{ODBC Driver 17 for SQL Server}'

    try:
        cnxn = pyodbc.connect('DRIVER=' + driver + 
                        ';SERVER=' + server + 
                        ';DATABASE=' + database + 
                        ';UID=' + username + 
                        ';PWD=' + password)

        cursor = cnxn.cursor()
        print('Connection established')
    except:
        print('Cannot connect to SQL server')
    print("INSERT INTO dbo.Product (ProductID, ProductName) VALUES ({0}, '{1}')".format(id,name))
    #cursor.execute("SET IDENTITY_INSERT dbo.Product ON")
    try : 
        cursor.execute("SET IDENTITY_INSERT dbo.Product ON")
        cursor.execute("INSERT INTO dbo.Product (ProductID, ProductName) VALUES ({0}, '{1}' )".format(id,name))
        cursor.execute("SET IDENTITY_INSERT dbo.Product OFF")
    except Exception as e :
        print(e)
        pass
    #cursor.execute("SET IDENTITY_INSERT dbo.Product OFF")
    cnxn.commit()
    cursor.close()

import pyodbc 

def deleteDataFromProducts(id) :
    server = 'tcp:sql-server-cloud.database.windows.net' 
    database = 'SQL-Database'
    username = 'ServerAdmin' 
    password = 'YouShallNotPass!'
    driver = '{ODBC Driver 17 for SQL Server}'

    try:
        cnxn = pyodbc.connect('DRIVER=' + driver + 
                        ';SERVER=' + server + 
                        ';DATABASE=' + database + 
                        ';UID=' + username + 
                        ';PWD=' + password)

        cursor = cnxn.cursor()
        print('Connection established')
    except:
        print('Cannot connect to SQL server')
    #cursor.execute("SET IDENTITY_INSERT dbo.Product ON")
    try : 
        cursor.execute("DELETE FROM dbo.Product WHERE ProductID = {0}".format(id))
    except Exception as e :
        print(e)
        pass
    #cursor.execute("SET IDENTITY_INSERT dbo.Product OFF")
    cnxn.commit()
    cursor.close()

