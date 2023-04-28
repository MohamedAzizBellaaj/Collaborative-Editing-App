import json

from PySide6.QtCore import Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QWidget

from RMQ_subscriber import RMQSubscriber
from section_ui import Ui_SectionWidget


class SectionWidget(QWidget, Ui_SectionWidget):
    update_ui = Signal(str)
    update_total_text = Signal(str, int)
    cleanup = Signal()

    def __init__(self, subscriber: RMQSubscriber, index: int):
        super().__init__()
        # Setup Ui
        self.setupUi(self)
        self.index = index
        self.identifier = f"Section {self.index}"
        self.label.setText(self.identifier)
        self.text_area.setReadOnly(True)
        self.confirm_button.setDisabled(True)

        # Declare subscriber/exchange/queues
        self.subscriber = subscriber
        self.exchange = f"{self.identifier}.exchange"
        self.update_queue = f"{self.subscriber.client_id}.{self.identifier}"
        self.occupied_by_queue = f"{self.identifier}.occupied_by"

        self.subscriber.declare_bind_queue_exchange(
            self.update_queue, self.exchange, True
        )
        self.subscriber.queue_declare(
            self.occupied_by_queue,
            arguments={"x-max-length": 1, "x-overflow": "reject-publish"},
        )
        self.subscriber.consumer.basic_consume(self.update_queue, self.on_consume, True)

        # Connecting Qt signals to slots
        self.text_area.textChanged.connect(self.on_edit_section)
        self.update_ui.connect(self.on_ui_update)
        self.cleanup.connect(self.on_cleanup)
        self.edit_button.clicked.connect(self.request_edit)
        self.confirm_button.clicked.connect(self.confirm_edit)

    def request_edit(self):
        payload = {"client": self.subscriber.client_id}
        self.subscriber.publisher.basic_publish(
            json.dumps(payload), self.occupied_by_queue
        )
        body = None
        method, properties, body = self.subscriber.basic_get(
            self.occupied_by_queue, auto_ack=False
        )
        self.subscriber.basic_nack(method.delivery_tag)
        body_payload = json.loads(body)
        if body_payload["client"] != self.subscriber.client_id:
            self.label.setText(
                f"{self.identifier} occupied by\n{body_payload['client']}"
            )
            self.edit_button.setDisabled(True)
        else:
            body_payload["lock"] = True
            self.subscriber.publisher.basic_publish(
                json.dumps(body_payload), exchange=self.exchange
            )
            self.update_editing_user_on_edit()

    def on_edit_section(self):
        payload = {
            "client": self.subscriber.client_id,
            "message": self.text_area.toPlainText(),
        }
        self.subscriber.publisher.basic_publish(
            json.dumps(payload), exchange=self.exchange
        )

    def confirm_edit(self):
        method, properties, body = self.subscriber.basic_get(
            self.occupied_by_queue, auto_ack=False
        )
        if body is not None:
            body_payload = json.loads(str(body, "utf-8"))
            if body_payload["client"] == self.subscriber.client_id:
                release_lock_payload = {
                    "client": self.subscriber.client_id,
                    "lock": False,
                }
                self.subscriber.basic_ack(method.delivery_tag)
                self.update_editing_user_on_confirm()
                self.subscriber.publisher.basic_publish(
                    json.dumps(release_lock_payload), exchange=self.exchange
                )
            else:
                self.subscriber.basic_nack(method.delivery_tag)

    def update_editing_user_on_edit(self):
        self.label.setText(f"{self.identifier} occupied by you!")
        self.text_area.setReadOnly(False)
        self.text_area.setFocus()
        cursor = self.text_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.text_area.setTextCursor(cursor)
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
        if payload["client"] == self.subscriber.client_id:
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

    def on_cleanup(self):
        self.confirm_edit()
