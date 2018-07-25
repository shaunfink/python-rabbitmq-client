import pika
import ssl

ssl_opts = {
    'ca_certs': 'certs/cacert.pem',
    'certfile': 'certs/cert.pem',
    'keyfile': 'certs/key.pem',
    'cert_reqs': ssl.CERT_REQUIRED,
    'ssl_version': ssl.PROTOCOL_TLSv1_2
}

rabbit_opts = {
    'host': 'rabbitmq.dev',
    'port': 5671,
    'user': 'rabbitdevcode',
    'password': 'rabbitdevcode',
    'virtual_host': 'devvhost',
}

rabbit_queue_opts = {
    'queue': 'python_ssl',
    'message': 'Hello SSL World :)'
}

#rabbit_creds = pika.PlainCredentials(rabbit_opts['user'], rabbit_opts['password'])
rabbit_creds = pika.credentials.ExternalCredentials()
parameters = pika.ConnectionParameters(host=rabbit_opts['host'],
                                       port=rabbit_opts['port'],
                                       credentials=rabbit_creds,
                                       virtual_host=rabbit_opts['virtual_host'],
                                       ssl=True,
                                       ssl_options=ssl_opts)

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=rabbit_queue_opts['queue'])

    channel.basic_publish(exchange='',
                          routing_key=rabbit_queue_opts['queue'],
                          body=rabbit_queue_opts['message'])

    print(" [x] Sent '" + rabbit_queue_opts['message'] + "!'")

    connection.close()
except BaseException as e:
    print(str(e), e.__class__.__name__)