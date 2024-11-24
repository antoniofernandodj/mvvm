import sys
from PySide6.QtWidgets import QApplication
from view import FileMongo


def main():
    app = QApplication(sys.argv)
    FileMongo().show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
