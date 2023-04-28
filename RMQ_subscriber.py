from pika import BlockingConnection
from pika.exchange_type import ExchangeType

from RMQ_consumer import RMQConsumer
from RMQ_publisher import RMQPublisher


class RMQSubscriber:
    def __init__(self, connection: BlockingConnection, client_id: str):
        self.client_id = client_id
        self.connection = connection
        self.channel = self.connection.channel()
        self.publisher = RMQPublisher(self.channel)
        self.consumer = RMQConsumer()

    def start_consume(self):
        self.consumer.start()

    def queue_declare(self, queue, durable=False, auto_delete=False, **args):
        name = self.channel.queue_declare(
            queue=queue, durable=durable, auto_delete=auto_delete, **args
        )
        return name.method.queue

    def exchange_declare(self, exchange, exchange_type):
        return self.channel.exchange_declare(
            exchange=exchange, exchange_type=exchange_type
        )

    def queue_delete(self, queue):
        self.channel.queue_delete(queue=queue)

    def bind_queue_exchange(self, queue, exchange):
        return self.channel.queue_bind(exchange=exchange, queue=queue)

    def declare_bind_queue_exchange(
        self, queue, exchange, auto_delete=False, exchange_type=ExchangeType.fanout
    ):
        self.queue_declare(queue=queue, auto_delete=auto_delete)
        self.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        self.bind_queue_exchange(exchange=exchange, queue=queue)

    def basic_get(self, queue, **args):
        return self.channel.basic_get(queue, **args)

    def basic_ack(self, tag, multiple=False):
        self.channel.basic_ack(tag, multiple)

    def basic_nack(self, tag, multiple=False):
        self.channel.basic_nack(tag, multiple)
