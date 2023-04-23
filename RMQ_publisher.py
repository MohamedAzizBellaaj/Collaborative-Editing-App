import pika


class RMQPublisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()

    def basic_publish(self, message, queue="", exchange=""):
        return self.channel.basic_publish(
            exchange=exchange, routing_key=queue, body=message
        )
