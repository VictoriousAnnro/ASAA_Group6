# Simple Kafka Consumer
import json
from kafka import KafkaConsumer
import time

def create_consumer():
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

def process_order(order):
    """Simple function to process an order (just prints it in this example)"""
    print(f"Processing order {order['order_id']} for {order['quantity']} units of {order['product']}")
    # In a real application, you might:
    # - Save to a database
    # - Send confirmation emails
    # - Update inventory
    # - Trigger shipping processes

def run_consumer():
    """Run the consumer, reading messages"""
    consumer = create_consumer()
    
    try:
        print("Consumer started. Waiting for messages...")
        # Continuously poll for new messages
        for message in consumer:
            order = message.value
            process_order(order)
            print(f"Received from partition {message.partition}, offset {message.offset}")
            print("---")
    except KeyboardInterrupt:
        print("Consumer stopped by user")
    finally:
        consumer.close()
        print("Consumer closed")

# Main execution
if __name__ == "__main__":
    # To run as a producer, uncomment:
    # run_producer()
    
    # To run as a consumer, uncomment:
    run_consumer()