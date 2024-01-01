from confluent_kafka import Producer
import time
from random import uniform
import random
from datetime import datetime 

status_choices = ["Strong : 3000Mbps", "Normal : 1000Mbps", "Weak : 50Mbps"]

# Cau hinh procedure
producer_config = {
    # Dia chi kafka broker
    'bootstrap.servers':'127.0.0.1:9092',
    'client.id':'python-producer'
}

# Khoi tao producer
producer = Producer(producer_config)

# Chu de kafka ma ban muon gui thong diep den
topic = 'abc'

# Gui thong diep theo chu de
for i in range(10):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    random_status = random.choice(status_choices)
    message = f'Status in: {current_time} {random_status}'
    producer.produce(topic, key=str(i), value=message)
    time.sleep(uniform(3, 5))

# Cho den khi tat ca cac thong diep da duoc gui
producer.flush()
print('Messages sent successfully')