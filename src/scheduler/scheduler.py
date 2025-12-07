import mysqlInterface as sqlInterface
import mongoDBInterface as mongoInterface
import json
from kafka import KafkaConsumer
from datetime import datetime

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
    print("scheduler timestamp:", ts)
    print(f"time it took: {datetime.fromtimestamp(ts - order['timestamp'])}")

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
