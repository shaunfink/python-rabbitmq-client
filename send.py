#!/usr/bin/env python
import logging
import pika

logging.basicConfig(level=logging.INFO)

credentials = pika.PlainCredentials('rabbitdevcode', 'rabbitdevcodeldap')
parameters = pika.ConnectionParameters('rabbitmq.dev', 5672, 'devvhost', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

print(" [x] Sent 'Hello World!'")

connection.close()
