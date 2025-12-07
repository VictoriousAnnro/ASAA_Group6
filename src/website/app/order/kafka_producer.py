# Simple Kafka Producer
import json
from kafka import KafkaProducer

def create_producer():
    """Create a connection to Kafka broker"""
    producer = KafkaProducer(
        #bootstrap_servers=['localhost:9092'],
        bootstrap_servers=['kafka:29092'],
        # Convert Python dict to JSON string and encode as bytes
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    return producer

def send_order(producer, car_title, model, engine, color, price):
    """Send a simple order message to Kafka"""
    # Create a sample order message
    # car_title, model, engine, color, price
    order = {
        'car_title': car_title,
        'model': model,
        'engine': engine,
        'color': color,
        'price': price
        #'order_id': order_id,
        #'chassisID': chassisID,  
        #'engineID': engineID,       
        #'interiorID': interiorID,          
        #'paintID': paintID       
    }
    
    # Send the order to the 'orders' topic
    # The order_id (as string) is used as the message key - NOT ANYMORE!!
    producer.send(
        'orders',                         # Topic name - DON'T CHANGE THIS!!
        #key=str(order_id).encode('utf-8'),  # Message key (optional)
        value=order                       # Message value
    )
    print(f"Sent order: {order}")
    
def run_producer(car_title, model, engine, color, price): # car_title, model, engine, color, price
    """Run the producer, sending a few messages"""
    producer = create_producer()
    
    try:
        # send message with order info
        send_order(producer, car_title, model, engine, color, price)
    finally:
        # Always flush and close the producer when done
        producer.flush()
        producer.close()
        print("Producer closed")