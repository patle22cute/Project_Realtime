from confluent_kafka import Consumer, KafkaError

# Configuration for the consumer
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': '1',
    'auto.offset.reset': 'earliest'
}

# Initialize the consumer
consumer = Consumer(consumer_config)

# Kafka topic you want to consume messages from
topic = 'projectDE'

# Subscribe to the topic
consumer.subscribe([topic])


while True:  # Set the exit condition
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('Reached the end of the partition')
        else:
            print(f'Error: {msg.error()}\n')
    else:
        message = msg.value().decode("utf-8") + '\n'
        with open('kafka/kafka-python/status_from_producer.txt', 'a') as file:
            file.write(message)
        print(f'{msg.value().decode("utf-8")}')

# Close the consumer
consumer.close()
