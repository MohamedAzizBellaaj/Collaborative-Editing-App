import threading

import pika
from pika.adapters.blocking_connection import BlockingChannel


class RMQConsumer(threading.Thread):
    def __init__(self):
        super(RMQConsumer, self).__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()

    def run(self):
        threading.Thread(target=self.channel.start_consuming, daemon=True).start()

    def basic_consume(self, queue, callback, auto_ack=True, **args):
        return self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=auto_ack, **args
        )

    def basic_get(self, queue, **args):
        return self.channel.basic_get(queue, **args)

    def basic_ack(self, tag, multiple=False):
        self.channel.basic_ack(tag, multiple)

    def basic_nack(self, tag):
        self.channel.basic_nack(tag)
