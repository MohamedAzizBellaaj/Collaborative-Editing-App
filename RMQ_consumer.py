import pika
from PySide6.QtCore import QThread


class RMQConsumer(QThread):
    def __init__(self):
        super(RMQConsumer, self).__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()

    def run(self):
        self.channel.start_consuming()

    def basic_consume(self, queue, callback, auto_ack=True, **args):
        return self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=auto_ack, **args
        )
