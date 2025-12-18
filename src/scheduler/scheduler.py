import mysqlInterface as sqlInterface
import mongoDBInterface as mongoInterface
import json
from kafka import KafkaConsumer
from datetime import datetime
from datetime import timedelta
import threading 
"""
ill be using threading for concurrency.
threads dont actually execute at the same time, rather python switches very quickly between the threads, making it appear as if theyre executing at the same time. Since the two methods scheduler uses to process the order each make contact with an external database, it makes sense to run these two methods in a thread, so that while the first method is awaiting a response from the database, the second method is also being executed instead of waiting.
Cons of this: We might set an order to be 'ready' before the recipe has even been saved. If smth goes wrong while saving the recipe, the order is still set as 'ready'. I think it's okay to have this con, as long as we're aware of it. In the real world, this would prolly be pretty bad for a customer website but alas. We all know school isn't real. 

PROBLEM - OrderStatus gets orderID from mongoDB, so it MUST wait for it. Is there a way to get the order.id from the database in the website and use that instead? 
 order = Order.objects.filter(customer=customer).order_by('-created_at').first()
 this object 'order' has an id. When is the object created and stored in DB, and when can we get access to the ID?
"""

# TODO
# is data persisted in volumes? Necessary?
# How to interract w kafka:
# https://medium.com/@hankimhak451/getting-started-with-apache-kafka-in-python-a-practical-guide-9e122067a3c0


# get order from website
# insert order in Orders
# insert recipe in mongodb
# insert order status in OrderStatus

# ===== KAFKA =====
# Scheduler is receiver in kafka
# while website is producer
"""
order = {
        'car_title': car_title,
        'model': model,
        'engine': engine,
        'color': color,
        'price': price
    }
    """

def createOrderConsumer():
    """Create a connection to Kafka broker as a consumer"""
    consumer = KafkaConsumer(
        'orders',                          # Topic to subscribe to
        #bootstrap_servers=['localhost:9092'],
        bootstrap_servers=['kafka:29092'],
        # Convert JSON bytes to Python dict
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        # Unique ID for this consumer group
        group_id='order-processing-group',
        # Start reading from the beginning of the topic
        auto_offset_reset='earliest'
    )
    return consumer

def processCustOrder(order):
    """Simple function to process an order (just prints it in this example)"""
    # car_title, model, engine, color, price
    print(f"Received order with {order['car_title']}, {order['model']}, {order['engine']}, {order['color']} and {order['price']} timestamp: {datetime.fromtimestamp(order['timestamp'])}")

    # save order in Orders
    #sqlInterface.saveCustomerOrder(order['order_id'], order['chassisID'], order['engineID'], order['interiorID'], order['paintID'])

    # Insert recipe in mongodb
    #mongoInterface.insertRecipe(order['order_id'], order['chassisID'], order['engineID'], order['interiorID'], order['paintID'])
    recipeID = mongoInterface.insertRecipe(order['car_title'], order['model'], order['engine'], order['color'])

    # put order in 'queue'
    sqlInterface.insertReadyOrder(recipeID)
    print(f"Order {recipeID} has been inserted in queue as 'ready'")
    print(f"Status for order {recipeID}: {sqlInterface.getOrderStatus(recipeID)}")

    # create timestamp
    # then compare to from website
    ts = datetime.now().timestamp()
    duration = ts - order['timestamp']

    #print("scheduler timestamp:", ts)
    print("scheduler timestamp:", datetime.fromtimestamp(ts))
    print("time it took:", timedelta(seconds=duration))
    print(f"time it took (numeric): {duration:.3f} seconds") #here, we should put the output in a file

    #ts = datetime.now().timestamp()
    #print("scheduler timestamp:", ts)
    #print(f"time it took: {datetime.fromtimestamp(ts - order['timestamp'])}")

def listenKafka():
    # Run the consumer, reading messages
    consumer = createOrderConsumer()

    try:
        print("Consumer started. Waiting for messages...")
        # Continuously poll for new messages
        for message in consumer:
            order = message.value
            processCustOrder(order)
            print(f"Received from partition {message.partition}, offset {message.offset}")
            print("---")
    except KeyboardInterrupt:
        print("Consumer stopped by user")
    finally:
        consumer.close()
        print("Consumer closed")

# ==================

# Get the oldest order that is 'ready'
def getNextReadyRecipe():
    orderID = sqlInterface.getOldestReadyOrder()

    recipe = mongoInterface.fetchRecipe(orderID)
    # TODO send recipe to orchestrator

    # update status to inProgress
    sqlInterface.changeOrderStatus(orderID, 'inProgress')

# ===== Wait for messages on Kafka ====
if __name__ == "__main__":
    print("scheduler running")
    listenKafka()
