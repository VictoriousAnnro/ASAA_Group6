import mysqlInterface as sqlInterface
import mongoDBInterface as mongoInterface

# TODO
# is data persisted in volumes? Necessary?
# How to interract w kafka

# For unknown reasons, app.py always tries to call db before it's up and running
# Need to re-launch app in docker desktop

# get order from website
# insert order in Orders
# insert recipe in mongodb
# insert order status in OrderStatus

# get 'ready' signal for orchestrator
# fetch oldest ready order, and send to orchestrator
# Update status to be 'inProgress'

def receiveCustOrder(order):
    # TODO - integration w kafka
    return None

def genRecipeFromOrder(order):
    sqlInterface.saveCustomerOrder(order) #order from kafka

    # Insert recipe in mongo
    mongoInterface.insertRecipe(order) # OR like (order.orderID, order.Cha)
    # Set order status 'ready'
    sqlInterface.insertReadyOrder(order.orderID)

# Get the oldest order that is 'ready'
def getNextReadyRecipe():
    orderID = sqlInterface.getOldestReadyOrder()

    recipe = mongoInterface.fetchRecipe(orderID)
    # TODO send recipe to orchestrator

    # update status to inProgress
    sqlInterface.changeOrderStatus(orderID, 'inProgress')

#mongoInterface.insertRecipe(3, 1, 2, 4, 3)
#rec = mongoInterface.fetchRecipe(3)
#print(rec)


#sqlInterface.insertReadyOrder(3)
#print("inserted order 3")
#status = sqlInterface.getOrderStatus('3')
#print(status)