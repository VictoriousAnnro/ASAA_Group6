# Simple Kafka Producer
import json
from kafka import KafkaProducer
import time

# DELETE THIS FILE LATER - JUST TO SEE EXAMPLE

def create_producer():
    """Create a connection to Kafka broker"""
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        # Convert Python dict to JSON string and encode as bytes
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    return producer

def send_order(producer, order_id):
    """Send a simple order message to Kafka"""
    # Create a sample order message
    order = {
        'order_id': order_id,
        'customer_id': f'customer-{order_id % 10}',  # Cycle through 10 customers
        'product': f'product-{order_id % 5}',        # Cycle through 5 products
        'quantity': (order_id % 3) + 1,              # 1-3 quantity
        'total': ((order_id % 3) + 1) * 10.99,       # Simple price calculation
        'timestamp': time.time()
    }
    
    # Send the order to the 'orders' topic
    # The order_id (as string) is used as the message key
    producer.send(
        'orders',                         # Topic name
        key=str(order_id).encode('utf-8'),  # Message key (optional)
        value=order                       # Message value
    )
    print(f"Sent order: {order}")
    
    # In production, you might want to handle errors with callbacks
    # future = producer.send('orders', value=order)
    # try:
    #     record_metadata = future.get(timeout=10)
    #     print(f"Message sent to {record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}")
    # except Exception as e:
    #     print(f"Error sending message: {e}")

def run_producer():
    """Run the producer, sending a few messages"""
    producer = create_producer()
    
    try:
        # Send 10 order messages
        for i in range(1, 11):
            send_order(producer, i)
            time.sleep(1)  # Wait a second between messages
    finally:
        # Always flush and close the producer when done
        producer.flush()
        producer.close()
        print("Producer closed")
# Main execution
if __name__ == "__main__":
    # To run as a producer, uncomment:
    run_producer()