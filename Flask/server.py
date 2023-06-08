from flask import Flask, render_template, request
from Customer_Sql import getCustomerData,writeDataIntoCustomers,deleteDataFromCustomers
from Resources_SQl import getResourceData, writeDataIntoResource , deleteDataResource
from Products_SQL import getProductsData , writeDataIntoProducts , deleteDataFromProducts
from get_all_sql_data import getAllSQLData
from refresh_Dropdowns_home import refresh
from refresh_Dropdowns_resources import refresh_resources
from write_new_Order import Submit_Order_to_Database

#Server.py hosted über die Flask libary die verschieden Websites für die Visualisierung und Eingabe von Daten in eine SQL-Datenbank
#Das Script ist dabei nicht in der Lage beliebige Datenbanken zu visualisieren, da die SQL-Abdfragen angepasst sind.7
#Diese Script Folgt dem Asatzt HTML/Jinja <-> Python <-> SQL <-> Datenbank  

app = Flask(__name__)

#Start des Servers auf der Start Website
@app.route("/")
@app.route("/home")
def home():
    customer, products = refresh() 
    return render_template("Website.html", CustomerIDs = customer, products=products)

#Weiterleiung an verschiedene Websites von der Home-Website über Buttons
@app.route("/sqlData",methods=['GET', 'POST'])
def sqlData():
    if request.method == 'POST':
        #Überprüfung welcher Button ausgewählt wurde
        if request.form['submit_button'] == 'SQL-Data':
            #Aktualisierung der Daten welche auf der Website geladen werden sollen, anternativ werden die Websites erstellt durch diesen Befehl
            getAllSQLData()
            #Öffnen der Website
            return render_template("sql-data.html")
        elif request.form['submit_button'] == 'Products':
            getProductsData()
            return render_template("products.html")
        elif request.form['submit_button'] == 'Customers':
            getCustomerData()
            return render_template("customers.html")
        elif request.form['submit_button'] == 'Resources':
            getResourceData()
            customer, products = refresh()
            resources, productsIds = refresh_resources()
            return render_template("resources.html",products=products, resources= resources, productIDs=productsIds)
        
@app.route("/sendOrder",methods=['GET', 'POST'])
def sendOrder() :
    output = request.form.to_dict()
    OrderID = output["OrderID"]
    CustomerID = output["CustomerID"]
    FirstName = output["FirstName"]
    LastName = output["LastName"]
    DateOfBirth = output["DateOfBirth"]
    ProductID = output["ProductID"]
    ProductName = output["ProductName"]
    PositionID = output["PositionID"]
    Amount = output["Amount"]
    Time = output["Time"]
    OrderID = output["OrderID"]

    return render_template("Website.html", OrderID = OrderID, CustomerID = CustomerID, FirstName= FirstName,LastName = LastName,DateOfBirth = DateOfBirth, ProductID = ProductID, ProductName = ProductName,PositionID = PositionID, Amount = Amount,Time = Time )

#Erstellen von neuen Aufträgen mit Daten eingegeben auf der Home-Website aktiviert durch Button auf der Home-Website
@app.route("/submitOrder",methods=['GET', 'POST'])
def submitOrder():
    output = request.form.to_dict()
    #Sammeln der Daten von Eingabefeldern
    Customer = request.form.get("Customer")
    Product1 = request.form.get("Product1")
    Amount1 = request.form.get("Amount1")
    Product2 = request.form.get("Product2")
    Amount2 = request.form.get("Amount2")
    Product3 = request.form.get("Product3")
    Amount3 = request.form.get("Amount3")
    #print(Product2)
    #print(Customer," ", Product1," ", Amount1," ", Product2," ", Amount2," ", Product3," ", Amount3 )
    #weiterleiten an Funktion damit ein SQL-QUERY durchgeführt wird
    Submit_Order_to_Database(Customer,Product1,Amount1,Product2,Amount2,Product3,Amount3)
    customer, products = refresh() 
    #neu laden der Website / leeren der Eingabefelder
    return render_template("Website.html", CustomerIDs = customer, products=products)


#######################################################################################################

#Die Folgenden Routes beziehen sich auf die Websites für die einzelnen Tabellen der Datenbank
#In diesen sind die Eingabe- und Löschfunktion der Buttons hinterlegt/ausgelöst

#Produkt-Tablle
@app.route("/products",methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        #Unterscheidung welcher Button ausgewählt wird
        if request.form['submit_button'] == 'Send':
            output = request.form.to_dict()
            ProductID = output["ProductID"]
            ProductName = output["ProductName"]
            writeDataIntoProducts(ProductID,ProductName)
            getProductsData()
            return render_template("products.html")
        if request.form['submit_button'] == 'Delete':
            output = request.form.to_dict()
            ProductID = output["Delete_ProductID"]
            deleteDataFromProducts(ProductID)
            getProductsData()
            return render_template("products.html")

#Customer-Tabelle
@app.route("/customers",methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Send':
            output = request.form.to_dict()
            CustomerID = output["CustomerID"]
            FirstName = output["FirstName"]
            LastName = output["LastName"]
            DateOfBirth = output["DateOfBirth"]
            writeDataIntoCustomers(CustomerID,FirstName,LastName,DateOfBirth)
            getCustomerData()
            return render_template("customers.html")
        if request.form['submit_button'] == 'Delete':
            output = request.form.to_dict()
            ProductID = output["Delete_CustomerID"]
            deleteDataFromCustomers(ProductID)
            getCustomerData()
            return render_template("customers.html")

#Resource-Tabelle
@app.route("/resources",methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Send':
            output = request.form.to_dict()
            ResourceID = output["ResourceID"]
            ProductID = request.form.get("Product")
            writeDataIntoResource(ResourceID,ProductID)
            getResourceData()
            customer, products = refresh()
            resources, productsIds = refresh_resources()
            return render_template("resources.html",products=products, resources= resources, productIDs=productsIds)
        if request.form['submit_button'] == 'Delete':
            output = request.form.to_dict()
            Rescource = request.form.get("Rescource")
            ProductID = request.form.get("ProductID")
            deleteDataResource(Rescource,ProductID)
            getResourceData()
            customer, products = refresh()
            resources, productsIds = refresh_resources()
            return render_template("resources.html", products=products, resources= resources, productIDs=productsIds)

if __name__ == '__main__' :
    app.run(debug= True, port= 50001)
