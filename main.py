import sys
import os
from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_dir = os.path.dirname(sys.argv[0])

    window = MainWindow(main_dir)
    window.show()

    app.exec()
