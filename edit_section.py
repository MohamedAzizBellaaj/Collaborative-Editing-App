import json

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from edit_section_ui import Ui_EditSectionWidget
from RMQ_connection import RMQConnection


class EditSectionWidget(QWidget, Ui_EditSectionWidget):
    update_text_area = Signal(str)
    update_total_text = Signal(str)

    def __init__(self, connection: RMQConnection, index: int):
        super().__init__()
        # Setup Ui
        self.setupUi(self)
        self.index = index
        self.identifier = f"section{self.index}"
        self.label.setText(self.identifier)
        self.text_area.setReadOnly(True)

        # Declare connection/queues/exchanges
        self.connection = connection
        self.exchange = f"exchange.{self.identifier}"
        self.update_queue = f"{self.connection.client_id}.{self.identifier}"
        self.occupied_by_queue = f"{self.identifier}.occupied_by"

        self.connection.declare_bind_queue_exchange(
            self.update_queue, self.exchange, True
        )
        self.connection.queue_declare(
            self.occupied_by_queue,
            arguments={"x-max-length": 1, "x-overflow": "reject-publish"}
        )
        self.connection.consumer.basic_consume(self.update_queue, self.on_consume, True)

        # Connecting Qt signals to slots
        self.text_area.textChanged.connect(self.on_edit_section)
        self.update_text_area.connect(self.on_update_value)
        self.edit_button.clicked.connect(self.request_edit)
        # self.confirm_button.connect(self.confirm_edit)

    def on_consume(self, ch, method, properties, body):
        payload = json.loads(body)
        if payload["client"] != self.connection.client_id:
            self.update_text_area.emit(payload["message"])

    def on_edit_section(self):
        payload = {
            "client": self.connection.client_id,
            "message": self.text_area.toPlainText(),
        }
        self.connection.publisher.basic_publish(
            json.dumps(payload),
            exchange=self.exchange,
        )

    def on_update_value(self, value: str):
        self.text_area.blockSignals(True)
        self.text_area.setText(value)
        self.text_area.blockSignals(False)
        self.update_total_text.emit(self.text_area.toPlainText())

    def request_edit(self):
        payload = {"client": self.connection.client_id}
        try:
            self.connection.publisher.basic_publish(json.dumps(payload),self.occupied_by_queue
            )
        except Exception:
            pass
        body = None
        try:
            method, properties, body = self.connection.consumer.basic_get(
                self.occupied_by_queue, auto_ack=False
            )
            self.connection.consumer.basic_nack(method.delivery_tag)
            print(body)
        except Exception:
            pass
        if body is None:
            self.text_area.setReadOnly(False)
            self.text_area.setFocus()
        
