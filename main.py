import sys

import pika
import qdarkstyle
from PySide6.QtWidgets import QApplication

from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside6"))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    main_window = MainWindow(app, connection)
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
