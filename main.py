import sys

import qdarkstyle
from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from RMQ_connection import RMQConnection


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside6"))
    connection = RMQConnection()
    main_window = MainWindow(app, connection)
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
