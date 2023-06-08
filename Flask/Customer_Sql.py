import pandas as pd
import pyodbc
import warnings

server = 'tcp:cloud4automationserver.database.windows.net' 
database = 'Cloud4AutomationDB'
username = 'cloud4automationadmin' 
password = 'keyword1!'
driver = '{ODBC Driver 17 for SQL Server}'

#Customer_Sql behinahlten die Funktionen zum lesen, schreiben und löschen der Customer-Tabelle in der Datenbank
#Die selbe Struktur wie Produkts SQL für mehr Kommentare dort schauen

def getCustomerData():
  warnings.filterwarnings('ignore')

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
    return query_result

  Product =readAnyTable("Customer")
  #Product.to_html("templates/sql-data.html")


  with open("templates/customers.html", 'w',encoding ='utf8') as _file:
      _file.write(
                  '<html>\n'
                  +'  <head><title>SQL-Data</title> <meta charset="utf-8"></head>\n'
                  +'  <link rel="stylesheet" type="text/css" href= "{0}"/>\n'.format("{{ url_for('static', filename='stylesheets/table.css') }}")
                  +'  <body>\n'
                  +'    <center>\n' 
                  +'    <h1> AzureSQL Database </h1><br><hr>'
                  +'    <h2> Customers </h2>\n'

                  +'    <form action="/customers" method="POST">\n'
                  +'    <input type="text" name="CustomerID" id="CustomerID" placeholder="CustomerID" />\n'
                  +'    <input type="text" name="FirstName" id="FirstName" placeholder="FirstName" />\n'
                  +'    <input type="text" name="LastName" id="LastName" placeholder="LastName" />\n'
                  +'    <input type="date" name="DateOfBirth" id="DateOfBirth" />\n'
                  +'    <input type="submit" value="Send" name="submit_button"/>\n'
                  +'    </form>\n'

                  +'    <form action="/customers" method="POST">\n'
                  +'    <input type="text" name="Delete_CustomerID" id="Delete_CustomerID" placeholder="CustomerID" />\n'
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
      
def writeDataIntoCustomers(id,Firstname,Lastname,Birthdate) :
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
    try :
        cursor.execute("SET IDENTITY_INSERT dbo.Customer ON")
        cursor.execute("INSERT INTO dbo.Customer (CustomerID, FirstName, LastName, DateOfBirth) VALUES ({0}, '{1}', '{2}', '{3}')".format(id,Firstname,Lastname,Birthdate)) 
        cursor.execute("SET IDENTITY_INSERT dbo.Customer OFF")
    except Exception as e :
        print(e)
        pass
    cnxn.commit()
    cursor.close()


def deleteDataFromCustomers(id) :
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
    try : 
        cursor.execute("DELETE FROM dbo.Customer WHERE CustomerID = '{0}'".format(id))
    except Exception as e :
        print(e)
        pass
    cnxn.commit()
    cursor.close()