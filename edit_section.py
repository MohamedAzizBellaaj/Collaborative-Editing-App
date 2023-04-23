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
        
        self.connection = connection
        self.exchange = f"exchange.{self.identifier}"
        self.update_queue = f"{self.connection.client_id}.{self.identifier}"
        self.occupied_by_queue = f"{self.identifier}.occupied_by"

        self.connection.declare_bind_queue_exchange(
            self.update_queue, self.exchange, True
        )
        self.connection.queue_declare(self.occupied_by_queue)
        self.connection.consumer.listen_queue(self.update_queue, self.on_consume, True)
        self.text_area.textChanged.connect(self.on_edit_section)
        self.update_text_area.connect(self.on_update_value)

    def on_consume(self, ch, method, properties, body):
        payload = json.loads(body)
        if payload["client"] != self.connection.client_id:
            self.update_text_area.emit(payload["message"])

    def on_edit_section(self):
        payload = {
            "client": self.connection.client_id,
            "message": self.text_area.toPlainText(),
        }
        self.connection.publisher.send_message(
            json.dumps(payload),
            exchange=self.exchange,
        )

    def on_update_value(self, value: str):
        self.text_area.blockSignals(True)
        self.text_area.setText(value)
        self.text_area.blockSignals(False)
        self.update_total_text.emit(self.text_area.toPlainText())


