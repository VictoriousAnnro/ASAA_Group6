import mysql.connector

config = {
        'user': 'root',
        'password': 'root',
        'host': 'mysqldb', #'db',
        'port': '3306',
        'database': 'mysqlDatabase'
}
dataBase = mysql.connector.connect(**config)

cursorObject = dataBase.cursor()

# we dont use this!
#def saveCustomerOrder(orderID, chassisID, engineID, interiorID, paintID):
#    cursorObject.execute(f"INSERT INTO Orders {orderID}, {chassisID}, {engineID}, {interiorID}, {paintID}")
    # I think below gives me syntax errors. Need to double-check if above works
    #query = """
    #INSERT INTO Orders (OrderID, chassisID, engineID, interiorID, paintID)
    #VALUES (%s, %s, %s, %s, %s)
    #"""
    #values = (orderID, chassisID, engineID, interiorID, paintID)
    #cursorObject.execute(query, values)
#    dataBase.commit()

def getCustomerOrder(OrderID):
    #cursorObject.execute("SELECT * FROM Orders WHERE orderID=%s", (OrderID))
    cursorObject.execute(f"SELECT * FROM Orders WHERE orderID={OrderID}")
    order=cursorObject.fetchone()

    return order

def insertReadyOrder(OrderID):
    cursorObject.execute(f"INSERT INTO OrderStatus (orderID, status) VALUES ('{OrderID}', 'ready')")
    #query = """
    #INSERT INTO OrderStatus (OrderID, Status)
    #VALUES (%s, %s)
    #"""
    #values = (OrderID, "ready")
    #cursorObject.execute(query, values)
    dataBase.commit()

def getOrderStatus(OrderID):
    cursorObject.execute(f"SELECT * FROM OrderStatus WHERE orderID='{OrderID}'")
    order=cursorObject.fetchone()

    # this gives me syntax error:
    #cursorObject.execute("SELECT status FROM OrderStatus WHERE orderID=%s", OrderID)
    #order=cursorObject.fetchone()

    return order

def getOldestReadyOrder():
    cursorObject.execute(f"SELECT orderID FROM OrderStatus WHERE status='ready' ORDER BY timestamp ASC LIMIT 1")
    orderID=cursorObject.fetchone()
    return orderID
    
def changeOrderStatus(OrderID, Status):
    cursorObject.execute(f"UPDATE OrderStatus SET status = {Status} WHERE orderID={OrderID}")

    dataBase.commit()