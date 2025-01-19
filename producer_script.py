from kafka import KafkaProducer
import json
import pandas as pd

df_csv = pd.read_csv('bank1.csv')
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
for index, row in df_csv.iterrows():
    record = {
        "DEPOSIT AMT": row[' DEPOSIT AMT '],
        "WITHDRAWAL AMT": row[' WITHDRAWAL AMT ']
    }
    producer.send('transactions', value=record)
    print(f"Sent: {record}")

    producer.flush()

producer.close()