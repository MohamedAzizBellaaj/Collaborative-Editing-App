import json
from tkinter import N

import pika
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
        self.confirm_button.setEnabled(False)

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
            arguments={"x-max-length": 1, "x-overflow": "reject-publish"},
        )
        self.connection.consumer.basic_consume(self.update_queue, self.on_consume, True)

        # Connecting Qt signals to slots
        self.text_area.textChanged.connect(self.on_edit_section)
        self.update_text_area.connect(self.on_update_ui)
        self.edit_button.clicked.connect(self.request_edit)
        self.confirm_button.clicked.connect(self.confirm_edit)

    def on_consume(self, ch, method, properties, body):
        payload = json.loads(body)
        if payload["client"] != self.connection.client_id:
            self.update_text_area.emit(json.dumps(payload))

    def on_edit_section(self):
        payload = {
            "client": self.connection.client_id,
            "message": self.text_area.toPlainText(),
        }
        self.connection.publisher.basic_publish(
            json.dumps(payload),
            exchange=self.exchange,
        )

    def on_update_ui(self, payload: str):
        payload = json.loads(payload)
        self.text_area.blockSignals(True)
        self.text_area.setText(payload["message"])
        self.text_area.blockSignals(False)
        self.update_total_text.emit(self.text_area.toPlainText())

    def request_edit(self):
        payload = {"client": self.connection.client_id}
        self.connection.publisher.basic_publish(
            json.dumps(payload), self.occupied_by_queue
        )
        body = None
        method, properties, body = self.connection.basic_get(
            self.occupied_by_queue, auto_ack=False
        )
        self.connection.basic_nack(method.delivery_tag)
        print(body, self.connection.client_id)
        if body is not None:
            body_payload = json.loads(body)
            if body_payload["client"] != self.connection.client_id:
                print(f"Its {body_payload['client']} turn")
                return
        # self.on_update_ui()
        self.text_area.setReadOnly(False)
        self.text_area.setFocus()
        self.toggle_edit_confirm_button_state()

    def confirm_edit(self):
        method, properties, body = self.connection.basic_get(
            self.occupied_by_queue, auto_ack=True
        )
        print(body, self.connection.client_id, "Released lock!")
        self.text_area.setReadOnly(True)
        self.toggle_edit_confirm_button_state()

    def toggle_edit_confirm_button_state(self):
        state = self.edit_button.isEnabled()
        self.edit_button.setEnabled(not state)
        self.confirm_button.setEnabled(state)
