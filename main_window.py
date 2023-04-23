from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QTextEdit, QVBoxLayout, QWidget

from edit_section import EditSectionWidget
from RMQ_connection import RMQConnection


class MainWindow(QMainWindow):
    def __init__(self, app, connection: RMQConnection):
        super().__init__()
        self.app = app
        self.connection = connection
        self.setup_ui()
        self.edit_section1.update_total_text.connect(self.update_text_1)
        self.edit_section2.update_total_text.connect(self.update_text_2)
        self.edit_section1.text_area.textChanged.connect(self.update_total_text)
        self.edit_section2.text_area.textChanged.connect(self.update_total_text)
        self.connection.start_consume()

    def setup_ui(self):
        self.setWindowTitle(f"Client {self.connection.client_id}")
        self.edit_section1 = EditSectionWidget(self.connection, 1)
        self.edit_section2 = EditSectionWidget(self.connection, 2)
        self.total_text = QTextEdit()
        self.total_text.setReadOnly(True)
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.edit_section1)
        v_layout.addWidget(self.edit_section2)
        h_layout = QHBoxLayout()
        h_layout.addLayout(v_layout)
        h_layout.addWidget(self.total_text)
        widget = QWidget()
        widget.setLayout(h_layout)
        self.setCentralWidget(widget)

    def update_text_1(self, value):
        self.total_text.setText(
            f"{value}\n{self.edit_section2.text_area.toPlainText()}"
        )

    def update_text_2(self, value):
        self.total_text.setText(
            f"{self.edit_section1.text_area.toPlainText()}\n{value}"
        )

    def update_total_text(self):
        self.total_text.setText(
            f"{self.edit_section1.text_area.toPlainText()}\n{self.edit_section2.text_area.toPlainText()}"
        )
