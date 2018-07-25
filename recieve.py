#!/usr/bin/env python
import logging
import pika

logging.basicConfig(level=logging.INFO)

credentials = pika.PlainCredentials('rabbitdevcode', 'rabbitdevcodelocal')
parameters = pika.ConnectionParameters('rabbitmq.dev', 5672, 'devvhost', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()