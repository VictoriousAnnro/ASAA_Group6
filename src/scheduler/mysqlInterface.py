import mysql.connector

config = {
        'user': 'root',
        'password': 'root',
        'host': 'mysqlDB',
        'port': '3306'
    }
 
dataBase = mysql.connector.connect(**config)

cursorObject = dataBase.cursor()

def getCustomerOrder(OrderID):
    cursorObject.execute("SELECT * FROM Orders WHERE OrderID=%s", (OrderID))
    order=cursorObject.fetchone()

    return order

def insertReadyOrder(OrderID):
    query = """
    INSERT INTO OrderStatus (OrderID, Status)
    VALUES (%s, %s)
    """
    values = (OrderID, "ready")
    cursorObject.execute(query, values)
    dataBase.commit()

def getOrderStatus(OrderID):
    cursorObject.execute("SELECT Status FROM OrderStatus WHERE OrderID=%s", (OrderID))
    order=cursorObject.fetchone()

    return order
    
def changeOrderStatus(OrderID, Status):
    query = """
    UPDATE OrderStatus SET Status = (Status) WHERE OrderID= (OrderID)
    VALUES (%s, %s)
    """
    values = (OrderID, Status)
    cursorObject.execute(query, values)
    dataBase.commit()