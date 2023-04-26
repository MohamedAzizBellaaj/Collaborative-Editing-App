import json

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from RMQ_connection import RMQConnection
from section_ui import Ui_SectionWidget


class SectionWidget(QWidget, Ui_SectionWidget):
    update_ui = Signal(str)
    update_total_text = Signal(str, int)
    clean_up = Signal()

    def __init__(self, connection: RMQConnection, index: int):
        super().__init__()
        # Setup Ui
        self.setupUi(self)
        self.index = index
        self.identifier = f"Section {self.index}"
        self.label.setText(self.identifier)
        self.text_area.setReadOnly(True)
        self.confirm_button.setDisabled(True)

        # Declare connection/exchange/queues
        self.connection = connection
        self.exchange = f"{self.identifier}.exchange"
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
        self.update_ui.connect(self.on_ui_update)
        self.clean_up.connect(self.on_clean_up)
        self.edit_button.clicked.connect(self.request_edit)
        self.confirm_button.clicked.connect(self.confirm_edit)

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
        body_payload = json.loads(body)
        if body_payload["client"] != self.connection.client_id:
            self.label.setText(
                f"{self.identifier} occupied by\n{body_payload['client']}"
            )
            self.edit_button.setDisabled(True)
        else:
            body_payload["lock"] = True
            self.connection.publisher.basic_publish(
                json.dumps(body_payload), exchange=self.exchange
            )
            self.update_editing_user_on_edit()

    def on_edit_section(self):
        payload = {
            "client": self.connection.client_id,
            "message": self.text_area.toPlainText(),
        }
        self.connection.publisher.basic_publish(
            json.dumps(payload), exchange=self.exchange
        )

    def confirm_edit(self):
        method, properties, body = self.connection.basic_get(
            self.occupied_by_queue, auto_ack=True
        )
        if body is not None:
            body_payload = json.loads(str(body, "utf-8"))
            if body_payload["client"] == self.connection.client_id:
                release_lock_payload = {
                    "client": self.connection.client_id,
                    "lock": False,
                }
                self.update_editing_user_on_confirm()
                self.connection.publisher.basic_publish(
                    json.dumps(release_lock_payload), exchange=self.exchange
                )

    def update_editing_user_on_edit(self):
        self.label.setText(f"{self.identifier} occupied by you!")
        self.text_area.setReadOnly(False)
        self.text_area.setFocus()
        self.toggle_edit_confirm_button_state()

    def update_editing_user_on_confirm(self):
        self.label.setText(f"{self.identifier}")
        self.text_area.setReadOnly(True)
        self.toggle_edit_confirm_button_state()

    def toggle_edit_confirm_button_state(self):
        state = self.edit_button.isEnabled()
        self.edit_button.setEnabled(not state)
        self.confirm_button.setEnabled(state)

    def on_consume(self, ch, method, properties, body):
        self.update_ui.emit(str(body, "utf-8"))

    def on_ui_update(self, payload: str):
        payload = json.loads(payload)
        if payload["client"] == self.connection.client_id:
            return
        if "lock" in payload:
            if payload["lock"]:
                self.label.setText(
                    f"{self.identifier} occupied by\n{payload['client']}"
                )
                self.edit_button.setDisabled(True)
            else:
                self.label.setText(self.identifier)
                self.edit_button.setEnabled(True)
        if "message" in payload:
            self.label.setText(f"{self.identifier} occupied by:\n{payload['client']}")
            self.edit_button.setDisabled(True)
            self.text_area.blockSignals(True)
            self.text_area.setText(payload["message"])
            self.text_area.blockSignals(False)
            self.update_total_text.emit(self.text_area.toPlainText(), self.index)

    def on_clean_up(self):
        self.confirm_edit()
