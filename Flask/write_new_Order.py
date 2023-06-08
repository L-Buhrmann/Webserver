import pyodbc
import pandas as pd
import warnings
from datetime import datetime

server = 'tcp:cloud4automationserver.database.windows.net' 
database = 'Cloud4AutomationDB'
username = 'cloud4automationadmin' 
password = 'keyword1!'
driver = '{ODBC Driver 17 for SQL Server}'

#Füllen von der Order und Position Tabelle in der Datenbank um einen Auftrag effizent zwischen zuspeichern
def Submit_Order_to_Database(CustomerID,Product1,Amount1,Product2,Amount2,Product3,Amount3):

    warnings.filterwarnings('ignore')

    #Lesenvon Tabellen
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
    
    #lesen der Order Tabelle um die nachfolgende OrderID zu bestimmmen
    Orders , conn = readAnyTable("Orders")
    Orders1, conn1 = readAnyTable("AllPositions") 
    #SELECT ProductID FROM [dbo].[Product] WHERE ProductName = 'Weiße Felge'
    CustomerID = CustomerID
    if  Orders.empty:
        OrderID = 1
    else :
        OrderID = Orders['OrderID'].values[-1] + 1
    try:
        if(OrderID <= Orders1['OrderID'].values[-1]): #OrderID < Orders1['OrderID'].values[-1]
            OrderID = Orders1['OrderID'].values[-1] + 1
    except:
        pass
    #Auslesen der Eingabezeit
    Time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #Füllen der Orders und Positions Tabellen mit den ermittelten Daten
    cursor = conn.cursor()
    cursor.execute("SET IDENTITY_INSERT dbo.Orders ON")
    cursor.execute("INSERT INTO dbo.Orders (OrderID, Date_and_Time, CustomerID) VALUES ({0}, '{1}', '{2}')".format(OrderID,Time,CustomerID))
    cursor.execute("SET IDENTITY_INSERT dbo.Orders OFF")
    #Füllen mehrere Zeilen in Position in abhängigkeit der Eingabe
    PositionNumber = 1
    if Product1 != "" and Amount1 != "" :
        ProductID1 = pd.read_sql_query('''  SELECT ProductID FROM[{0}].[dbo].[Product] WHERE ProductName = '{1}' '''.format(database,Product1), conn)
        print(ProductID1['ProductID'].values[0])
        cursor.execute("INSERT INTO dbo.Position (OrderID, PositionID, ProductID, Amount) VALUES ({0}, {1}, {2}, {3})".format(OrderID,PositionNumber,ProductID1['ProductID'].values[0],Amount1))
        PositionNumber = PositionNumber + 1
    if (Product2 != "") and (Amount2 != "") :
        print("Test2")
        print(Amount2)
        print(Product2)
        ProductID2 = pd.read_sql_query('''  SELECT ProductID FROM[{0}].[dbo].[Product] WHERE ProductName = '{1}' '''.format(database,Product2), conn)
        cursor.execute("INSERT INTO dbo.Position (OrderID, PositionID, ProductID, Amount) VALUES ({0}, {1}, {2}, {3})".format(OrderID,PositionNumber,ProductID2['ProductID'].values[0],Amount2))
        PositionNumber = PositionNumber + 1
    if (Product3 != "") and (Amount3 != "") :
        print("Test3")
        ProductID3 = pd.read_sql_query('''  SELECT ProductID FROM[{0}].[dbo].[Product] WHERE ProductName = '{1}' '''.format(database,Product3), conn)
        cursor.execute("INSERT INTO dbo.Position (OrderID, PositionID, ProductID, Amount) VALUES ({0}, {1}, {2}, {3})".format(OrderID,PositionNumber,ProductID3['ProductID'].values[0],Amount3))
        PositionNumber = PositionNumber + 1

    #cursor.execute("SET IDENTITY_INSERT dbo.Product OFF")s
    conn.commit()
    cursor.close()

