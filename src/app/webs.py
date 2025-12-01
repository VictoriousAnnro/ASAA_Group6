# Simple Kafka Producer
import json
from kafka import KafkaProducer

def create_producer():
    """Create a connection to Kafka broker"""
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        # Convert Python dict to JSON string and encode as bytes
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    return producer

def send_order(producer, order_id, chassisID, engineID, interiorID, paintID):
    """Send a simple order message to Kafka"""
    # Create a sample order message
    order = {
        'order_id': order_id,
        'chassisID': chassisID,  
        'engineID': engineID,       
        'interiorID': interiorID,          
        'paintID': paintID       
    }
    
    # Send the order to the 'orders' topic
    # The order_id (as string) is used as the message key
    producer.send(
        'orders',                         # Topic name - DON'T CHANGE THIS!!
        key=str(order_id).encode('utf-8'),  # Message key (optional)
        value=order                       # Message value
    )
    print(f"Sent order: {order}")
    
def run_producer(producer, order_id, chassisID, engineID, interiorID, paintID):
    """Run the producer, sending a few messages"""
    producer = create_producer()
    
    try:
        #TODO send message with order info
        # send_order(...)
        print("lol")
    finally:
        # Always flush and close the producer when done
        producer.flush()
        producer.close()
        print("Producer closed")

# TODO call run_producer to send an order to scheduler