import docker

# Khởi tạo Docker client
client = docker.from_env()

# Bước 1: Khởi động container Spark-Master
spark_master_container = client.containers.run('bde2020/spark-master:latest', detach=True)

# Bước 2: Lấy địa chỉ IP của container Spark-Master
spark_master_ip = spark_master_container.attrs['NetworkSettings']['IPAddress']

# Bước 3: Khởi động container Kafka và liên kết nó với container Spark-Master
kafka_container = client.containers.run('wurstmeister/kafka:latest',
                                        detach=True,
                                        environment={'KAFKA_ADVERTISED_HOST_NAME': spark_master_ip},
                                        links={'spark-master': 'spark-master'})

# Bước 4: Kiểm tra kết nối
kafka_logs = kafka_container.logs().decode('utf-8')
print(kafka_logs)