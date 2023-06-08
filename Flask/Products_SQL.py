
import pandas as pd
import pyodbc
import warnings

server = 'tcp:cloud4automationserver.database.windows.net' 
database = 'Cloud4AutomationDB'
username = 'cloud4automationadmin' 
password = 'keyword1!'
driver = '{ODBC Driver 17 for SQL Server}'

#Products_SQL behinahlten die Funktionen zum lesen, schreiben und löschen der Product-Tabelle in der Datenbank


#Die Funktion zum auslesen der Datenbank schreibt nach dem Ausledern der Daten die Webseite resources.html für die Darstellung um 
def getProductsData():
  warnings.filterwarnings('ignore')

  def readAnyTable(tablename):
    #Verbindung mit der Datenbank aufbauen
    conn = pyodbc.connect('DRIVER=' + driver + 
                        ';SERVER=' + server + 
                        ';DATABASE=' + database + 
                        ';UID=' + username + 
                        ';PWD=' + password)
    #Auslesen einer Tabelle und einfügen dieser in eine Pandas Datenstruktur 
    query_result = pd.read_sql_query(
              ''' 
                  SELECT *
                  FROM [{0}].[dbo].[{1}]
              '''.format(database,tablename), conn)
    print(query_result)
    return query_result

  Product =readAnyTable("Product")
  #Product.to_html("templates/sql-data.html")

  #Erstellen der Webseite mit aktualierten Daten Datenstruktur wird in hmtl-Code übersetzt
  with open("templates/products.html", 'w',encoding ='utf8') as _file:
      _file.write(
                  '<html>\n'
                  +'  <head><title>SQL-Data</title> <meta charset="utf-8"></head>\n'
                  +'  <link rel="stylesheet" type="text/css" href= "{0}"/>\n'.format("{{ url_for('static', filename='stylesheets/table.css') }}")
                  +'  <body>\n'
                  +'    <center>\n' 
                  +'    <h1> AzureSQL Database </h1><br><hr>'
                  +'    <h2> Products </h2>\n'

                  +'    <form action="/products" method="POST">\n'
                  +'    <input type="text" name="ProductID" id="ProductID" placeholder="ProductID" />\n'
                  +'    <input type="text" name="ProductName" id="ProductName" placeholder="ProductName" />\n'
                  +'    <input type="submit" value="Send" name="submit_button"/>\n'
                  +'    </form>\n'

                  +'    <form action="/products" method="POST">\n'
                  +'    <input type="text" name="Delete_ProductID" id="Delete_ProductID" placeholder="ProductID" />\n'
                  +'    <input type="submit" value="Delete" name="submit_button"/>\n'
                  +'    </form>\n'

                  + Product.to_html(index=False,border=2,justify="center") + '<br><hr>\n'
                  +'    <form action="/home">\n'
                  +'    <input type="submit" value="Back" name="action1"/>\n'
                  +'    </form>\n'
                  +'    </center>\n'
                  +'  </body>\n'
                  +'</html>\n'
                  )

#Befüllen der Tablle mit neuen Daten
def writeDataIntoProducts(id,name) :

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
        #SQL-Code zum Manipulieren der Datenbank
        cursor.execute("SET IDENTITY_INSERT dbo.Product ON")
        cursor.execute("INSERT INTO dbo.Product (ProductID, ProductName) VALUES ({0}, '{1}' )".format(id,name))
        cursor.execute("SET IDENTITY_INSERT dbo.Product OFF")
    except Exception as e :
        print(e)
        pass
    #cursor.execute("SET IDENTITY_INSERT dbo.Product OFF")
    #Ausführen des SQL-Codes
    cnxn.commit()
    cursor.close()

#Löschen von Daten aus der Tabelle einer Datenbank
def deleteDataFromProducts(id) :

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


