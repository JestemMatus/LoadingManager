import logging
import sys
import time
import os
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QVariant, pyqtSlot, QUrl
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication, QPushButton
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from loading_manager import LoadingManager


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class WebBridge(QObject):
    """
    Bridge for communication between Python and JavaScript in the QWebEngineView.
    """
    send_data_to_js = pyqtSignal(QVariant)
    receive_data = pyqtSignal(str, str)

    def __init__(self, data):
        super().__init__()
        self._data = data

    @pyqtSlot()
    def send_data(self):
        """
        Sends data to the JavaScript side if available.
        """
        if self._data:
            self.send_data_to_js.emit(self._data)
        else:
            logging.error("No data to send!")

    @pyqtSlot(str, str)
    def receive_data_from_js(self, selected_location, selected_role):
        """
        Receives data from the JavaScript side.
        """
        if selected_role and selected_location:
            self.receive_data.emit(selected_location, selected_role)
        else:
            logging.error("Invalid data received!")


def prepare_to_open_next_window():
    """
    Simulates a delay before opening the nextWindow.
    """
    logging.info("Simulating delay before opening NextWindow")
    time.sleep(3)


class MainWindow(QDialog):
    """
    A dialog for selecting a role and location. Uses QWebEngineView for displaying the UI.
    """

    def __init__(self, edit_callback, parent=None):
        super().__init__(parent)
        self.bridge = None
        self.channel = None
        self.web_view = None
        logging.info("Initializing MainWindow")
        self.next_window = None
        self.edit_callback = edit_callback
        self.selected_location = None
        self.layout = QVBoxLayout(self)
        self.init_ui()
        self.show()

    def init_ui(self):
        """
        Initializes the UI by loading a page and setting up the web view.
        """
        loading_manager = LoadingManager(self.prepare_to_open_new_page)
        success = loading_manager.execute()
        logging.info(f"Loading result in MainWindow: {success}")
        if success:
            self.initialize_ui()
        else:
            logging.error("Failed to open new page in MainWindow")

    @staticmethod
    def prepare_to_open_new_page():
        """
        Simulates a delay before opening a new page.
        """
        time.sleep(3)

    def initialize_ui(self):
        """
        Initializes the user interface and sets up the QWebEngineView.
        """
        logging.info("Initializing UI - MainWindow")
        self.web_view = QWebEngineView()
        self.channel = QWebChannel()
        self.setWindowTitle("MainWindow")

        data = None  # Placeholder for actual data

        self.bridge = WebBridge(data)
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)
        self.layout.addWidget(self.web_view)

        html_content = """<html><body><h1>Main Window HTML</h1></body></html>"""
        base_url = QUrl.fromLocalFile(os.getcwd() + "/")
        self.web_view.setHtml(html_content, baseUrl=base_url)

        self.setup_web_view()

    def setup_web_view(self):
        """
        Sets up the web view and adds a button for interaction.
        """
        logging.info("Setting up web view with a button in MainWindow")
        button = QPushButton("Click to close and open nextWindow")
        button.clicked.connect(self.open_next_window)
        self.layout.addWidget(button)

    def open_next_window(self):
        """
        Handles the button click event to close this window and open the next one.
        """
        logging.info("Button clicked - closing MainWindow and opening NextWindow")
        loading_manager = LoadingManager(prepare_to_open_next_window)
        success = loading_manager.execute()
        logging.info(f"Loading result for NextWindow: {success}")
        if success:
            self.close()
            self.next_window = NextWindow(self.edit_callback)
            self.next_window.show()
        else:
            logging.error("Failed to open NextWindow")


class NextWindow(QDialog):
    """
    A dialog for displaying the nextWindow with a simple web view.
    """

    def __init__(self, edit_callback=None, parent=None):
        super().__init__(parent)
        self.bridge = None
        self.channel = None
        self.web_view = None
        logging.info("Initializing NextWindow")
        self.edit_callback = edit_callback
        self.layout = QVBoxLayout(self)
        self.initialize_ui()

    def initialize_ui(self):
        """
        Initializes the user interface and sets up the QWebEngineView.
        """
        logging.info("Initializing UI - NextWindow")
        self.web_view = QWebEngineView()
        self.channel = QWebChannel()
        self.setWindowTitle("NextWindow")

        data = None

        self.bridge = WebBridge(data)
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)
        self.layout.addWidget(self.web_view)

        html_content = """<html><body><h1>Next Window</h1></body></html>"""
        self.web_view.setHtml(html_content)


if __name__ == '__main__':
    def dummy_edit_callback():
        logging.info("Edit callback triggered")

    app = QApplication(sys.argv)
    main_window = MainWindow(dummy_edit_callback)
    sys.exit(app.exec_())
