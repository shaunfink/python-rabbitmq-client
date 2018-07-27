# Copyright 2017-2018 Andreas Sekulski
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    'queue': 'python_ssl'
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

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)


    channel.basic_consume(callback,
                          queue=rabbit_queue_opts['queue'],
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

except BaseException as e:
    print(str(e), e.__class__.__name__)
