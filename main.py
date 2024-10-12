import logging
import sys
from PyQt5.QtWidgets import QApplication
from loading_test import MainWindow

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def dummy_edit_callback():
    logging.info("Edit callback triggered")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow(dummy_edit_callback)
    sys.exit(app.exec_())
