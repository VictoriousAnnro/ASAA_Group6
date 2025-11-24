import mysqlInterface as mysqlDBint
import mongoDBInterface as mongoDB

# get order from website
# insert order in Orders
# create recipe
# insert recipe in mongodb
# insert order status in OrderStatus

def test():
    mysqlDBint.insertReadyOrder(3)
    print("inserted order 3")
    status = mysqlDBint.getOrderStatus(3)
    print(status)