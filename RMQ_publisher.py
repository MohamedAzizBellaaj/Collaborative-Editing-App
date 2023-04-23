from pika.adapters.blocking_connection import BlockingChannel


class RMQPublisher:
    def __init__(self, channel: BlockingChannel):
        self.channel = channel

    def send_message(self, message, queue="", exchange=""):
        return self.channel.basic_publish(
            exchange=exchange, routing_key=queue, body=message
        )
