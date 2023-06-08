import pandas as pd
import pyodbc
import warnings



#Die Funktion ließt mehrere Tabellen von der Datenbank aus und erstellt mit den Daten ein HTML skript
def getAllSQLData():
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
    print(query_result)#
    return query_result

  #Auslesen der Tabellen aus der Datenbank

  Customer = readAnyTable("Customer")
  #Customer.to_html("templates/sql-data.html")
  Orders= readAnyTable("Orders")
  #Orders.to_html("templates/sql-data.html")
  Product =readAnyTable("Product")
  #Product.to_html("templates/sql-data.html")
  Position = readAnyTable("Position")
  #Position.to_html("templates/sql-data.html")
  Resource = readAnyTable("Resource")
  "{{ url_for('static', filename='stylesheets/style.css') }}"

  #Erstellen des HTML-Script mit den Daten aus den Tabllen
  with open("templates/sql-data.html", 'w',encoding ='utf8') as _file:
      _file.write(
                  '<html>\n'
                  +'  <head><title>SQL-Data</title> <meta charset="utf-8"></head>\n'
                  +'  <link rel="stylesheet" type="text/css" href= "{0}"/>\n'.format("{{ url_for('static', filename='stylesheets/table.css') }}")
                  +'  <body>\n'
                  +'    <center>\n' 
                  +'    <h1> AzureSQL Database </h1><br><hr>'
                  +'    <h2> Customer </h2>\n' 
                  + Customer.to_html(index=False,border=2,justify="center") + '<be><hr>\n'
                  +'    <h2> Orders </h2>\n' 
                  + Orders.to_html(index=False,border=2,justify="center") + '<br><hr>\n'
                  +'    <h2> Product </h2>\n' 
                  + Product.to_html(index=False,border=2,justify="center") + '<br><hr>\n'
                  +'    <h2> Position </h2>\n' 
                  + Position.to_html(index=False,classes="redTable",border=2,justify="center") + '<br><hr>\n'
                  +'    <h2> Resource </h2>\n' 
                  + Resource.to_html(index=False,classes="redTable",border=2,justify="center") + '<br><hr>\n' 
                  +'    <form action="/home">\n'
                  +'    <input type="submit" value="Back" name="action1"/>\n'
                  +'    </form>\n'
                  +'    </center>\n'
                  +'  </body>\n'
                  +'</html>\n'
                  )

