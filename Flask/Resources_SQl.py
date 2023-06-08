import pandas as pd
import pyodbc
import warnings

server = 'tcp:cloud4automationserver.database.windows.net' 
database = 'Cloud4AutomationDB'
username = 'cloud4automationadmin' 
password = 'keyword1!'
driver = '{ODBC Driver 17 for SQL Server}'

#Resources_SQl behinahlten die Funktionen zum lesen, schreiben und löschen der Resource-Tabelle in der Datenbank
#Die selbe Struktur wie Produkts SQL für mehr Kommentare dort schauen

def getResourceData():
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

  Product =readAnyTable("Resource")
  #Product.to_html("templates/sql-data.html")


  with open("templates/resources.html", 'w',encoding ='utf8') as _file:
    _file.write(
        '<html>\n'
        +'  <head><title>SQL-Data</title> <meta charset="utf-8"></head>\n'
        +'  <link rel="stylesheet" type="text/css" href= "{0}"/>\n'.format("{{ url_for('static', filename='stylesheets/table.css') }}")
        +'  <body>\n'
        +'    <center>\n' 
        +'    <h1> AzureSQL Database </h1><br><hr>'
        +'    <h2> Resources </h2>\n'

        +'    <form action="/resources" method="POST">\n'
        +'    <input type="text" name="ResourceID" id="ResourceID" placeholder="ResourceID" />\n'
        +'    {% if products %}'
        +'    <select name="Product" id="Product-select">\n'
        +'    <option value="">--Please choose an Product--</option>'
        +'     {% for i in products %}\n'
        +'    <option value="{{i}}">{{i}}</option>\n'
        +'    {% endfor %}\n'
        +'    </select>\n'
        +'    {% endif %}\n'
        +'    <input type="submit" value="Send" name="submit_button"/>\n'
        +'    </form>\n'

        +'    <form action="/resources" method="POST">\n'

        +'    {% if resources %}'
        +'    <select name="Rescource" id="Product-select">\n'
        +'    <option value="">--Please choose an Rescource--</option>'
        +'     {% for i in resources %}\n'
        +'    <option value="{{i}}">{{i}}</option>\n'
        +'    {% endfor %}\n'
        +'    </select>\n'
        +'    {% endif %}\n'

        +'    {% if productIDs %}'
        +'    <select name="ProductID" id="Product-select">\n'
        +'    <option value="">--Please choose an ProductID--</option>'
        +'     {% for i in productIDs %}\n'
        +'    <option value="{{i}}">{{i}}</option>\n'
        +'    {% endfor %}\n'
        +'    </select>\n'
        +'    {% endif %}\n'

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
      
def writeDataIntoResource(ResourceID,Product) :
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
        ProductID = pd.read_sql_query('''  SELECT ProductID FROM[{0}].[dbo].[Product] WHERE ProductName = '{1}' '''.format(database,Product), cnxn)
        print(ProductID)
        cursor.execute("INSERT INTO dbo.Resource (ResourceID, ProductID) VALUES ('{0}', {1})".format(ResourceID,ProductID['ProductID'].values[0])) 
    except Exception as e :
        print(e)
        pass
    #cursor.execute("SET IDENTITY_INSERT dbo.Product OFF")
    cnxn.commit()
    cursor.close()


def deleteDataResource(resource, product) :

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
        cursor.execute("DELETE FROM dbo.Resource WHERE ResourceID = '{0}' AND ProductID = '{1}'".format(resource,product))
    except Exception as e :
        print(e)
        pass
    #cursor.execute("SET IDENTITY_INSERT dbo.Product OFF")
    cnxn.commit()
    cursor.close()