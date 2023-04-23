import threading

from pika.adapters.blocking_connection import BlockingChannel


class RMQConsumer(threading.Thread):
    def __init__(self, channel: BlockingChannel):
        super(RMQConsumer, self).__init__()
        self.channel = channel

    def run(self):
        threading.Thread(target=self.channel.start_consuming, daemon=True).start()

    def listen_queue(self, queue, callback, auto_ack=True, **args):
        return self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=auto_ack, **args
        )

    def basic_ack(self, tag, multiple=False):
        self.channel.basic_ack(tag, multiple)
