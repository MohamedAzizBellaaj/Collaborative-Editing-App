import uuid

from pika import BlockingConnection
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QTextEdit, QVBoxLayout, QWidget

from RMQ_subscriber import RMQSubscriber
from section import SectionWidget

NUMBER_OF_SECTIONS = 3


class MainWindow(QMainWindow):
    def __init__(self, app, connection: BlockingConnection):
        super().__init__()
        self.app = app
        self.connection = connection
        self.setup()
        for section in self.sections:
            section.update_total_text.connect(self.update_text)
            section.text_area.textChanged.connect(self.update_total_text)

    def setup(self):
        self.client_id = str(uuid.uuid4())
        self.setWindowTitle(f"Client {self.client_id}")
        self.sections = []
        for i in range(NUMBER_OF_SECTIONS):
            subscriber = RMQSubscriber(self.connection, self.client_id)
            section = SectionWidget(subscriber, i + 1)
            section.subscriber.start_consume()
            self.sections.append(section)

        self.total_text = QTextEdit()
        self.total_text.setReadOnly(True)
        v_layout = QVBoxLayout()
        for section in self.sections:
            v_layout.addWidget(section)
        h_layout = QHBoxLayout()
        h_layout.addLayout(v_layout)
        h_layout.addWidget(self.total_text)
        widget = QWidget()
        widget.setLayout(h_layout)
        self.setCentralWidget(widget)

    def update_text(self, value, id):
        index = id - 1
        text = ""
        for num, section in enumerate(self.sections):
            if num == index:
                text += f"{value}\n"
            else:
                text += f"{section.text_area.toPlainText()}\n"
        self.total_text.setText(text)

    def update_total_text(self):
        text = ""
        for section in self.sections:
            text += f"{section.text_area.toPlainText()}\n"
        self.total_text.setText(text)

    def closeEvent(self, event):
        for section in self.sections:
            section.cleanup.emit()
        event.accept()
