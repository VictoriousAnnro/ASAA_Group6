import mysqlInterface as sqlInterface
import mongoDBInterface as mongoInterface
import json
from kafka import KafkaConsumer
import time

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

"""order = {
    'order_id': lol,
    'chassisID': lol,
    'engineID': lol,
    'interiorID': lol,
    'paintID': lol
}"""

def createOrderConsumer():
    """Create a connection to Kafka broker as a consumer"""
    consumer = KafkaConsumer(
        'orders',                          # Topic to subscribe to
        bootstrap_servers=['localhost:9092'],
        # Convert JSON bytes to Python dict
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        # Unique ID for this consumer group
        group_id='order-processing-group',
        # Start reading from the beginning of the topic
        auto_offset_reset='earliest'
    )
    return consumer

def processCustOrder(order):
    # save order in Orders
    sqlInterface.saveCustomerOrder(order['order_id'], order['chassisID'], order['engineID'], order['interiorID'], order['paintID'])

    # Insert recipe in mongodb
    mongoInterface.insertRecipe(order['order_id'], order['chassisID'], order['engineID'], order['interiorID'], order['paintID'])

    # put order in 'queue'
    sqlInterface.insertReadyOrder(order['order_id'])


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
    listenKafka()

#mongoInterface.insertRecipe(3, 1, 2, 4, 3)
#rec = mongoInterface.fetchRecipe(3)
#print(rec)


#sqlInterface.insertReadyOrder(3)
#print("inserted order 3")
#status = sqlInterface.getOrderStatus('3')
#print(status)