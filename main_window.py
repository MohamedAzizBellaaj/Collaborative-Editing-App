from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QTextEdit, QVBoxLayout, QWidget

from RMQ_connection import RMQConnection
from section import SectionWidget


class MainWindow(QMainWindow):
    def __init__(self, app, connection: RMQConnection):
        super().__init__()
        self.app = app
        self.connection = connection
        self.setup_ui()
        for section in self.sections:
            section.update_total_text.connect(self.update_text)
        self.sections[0].text_area.textChanged.connect(self.update_total_text)
        self.sections[1].text_area.textChanged.connect(self.update_total_text)
        self.connection.start_consume()

    def setup_ui(self):
        self.setWindowTitle(f"Client {self.connection.client_id}")
        number_sections = 3
        self.sections = []
        for i in range(number_sections):
            section = SectionWidget(self.connection, i + 1)
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
            section.clean_up.emit()
        event.accept()
