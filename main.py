import sys

from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from RMQ_connection import RMQConnection


def main():
    app = QApplication(sys.argv)
    connection = RMQConnection()
    main_window = MainWindow(app, connection)
    main_window.show()

    app.exec()


if __name__ == "__main__":
    main()
