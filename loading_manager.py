import logging
import sys
import time
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineWidgets import QWebEngineView
from progressbar_style import html_content

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class LoadingManager:
    """
    Manages the execution of a long-running task in a separate thread and displays a loading dialog.
    """

    def __init__(self, function, *args, **kwargs):
        """
        Initializes the LoadingManager with the function to execute and its arguments.

        Args:
            function (callable): The function to be executed in the background thread.
            *args: Arguments for the function.
            **kwargs: Keyword arguments for the function.
        """
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.dialog = None
        self.result = None

    class WorkerThread(QThread):
        """
        A QThread that executes the given function in the background and emits a signal when finished.
        """
        finished = pyqtSignal(bool)

        def __init__(self, function, *args, **kwargs):
            super().__init__()
            self.function = function
            self.args = args
            self.kwargs = kwargs

        def run(self):
            """
            Executes the function in the background and emits the finished signal.
            """
            try:
                logging.info("WorkerThread has started executing the task.")
                self.function(*self.args, **self.kwargs)
                logging.info("WorkerThread has finished executing the task.")
                self.finished.emit(True)
            except Exception as e:
                logging.exception("Exception occurred during task execution.")
                self.finished.emit(False)

    def execute(self):
        """
        Starts the worker thread, shows the dialog, and synchronizes between the thread and the GUI.

        Returns:
            bool: The result of the task execution.
        """
        logging.info("Starting LoadingManager execution.")
        self.dialog = LoadingDialog()  # Create a new dialog for each execution
        self.thread = self.WorkerThread(self.function, *self.args, **self.kwargs)
        self.thread.finished.connect(self.handle_finished)
        self.thread.start()
        logging.info("WorkerThread started in LoadingManager.")
        self.dialog.exec_()  # Show the dialog
        return self.result

    def handle_finished(self, result):
        """
        Handles the finished signal, closes the dialog, and stores the result.

        Args:
            result (bool): The result of the thread's execution.
        """
        self.result = result if result is not None else True  # Treat None as success
        logging.info("Closing dialog.")
        self.dialog.accept()  # Close the dialog after the thread finishes


class LoadingDialog(QDialog):
    """
    A loading dialog that displays a message during long-running tasks using HTML.
    """

    def __init__(self):
        super().__init__()
        self.web_view = None
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setModal(True)
        self.resize(700, 220)
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface with QWebEngineView to display the HTML content.
        """
        layout = QVBoxLayout(self)

        self.web_view = QWebEngineView()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.web_view.page().setBackgroundColor(Qt.transparent)
        layout.addWidget(self.web_view)
        self.setLayout(layout)

        self.web_view.setHtml(html_content)

    def closeEvent(self, event):
        """
        Closes the QWebEngineView and releases resources when the dialog is closed.
        """
        if self.web_view:
            self.web_view.page().deleteLater()
            self.web_view.deleteLater()
            self.web_view = None
            logging.info("Resources for QWebEngineView have been released.")
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    def long_running_task():
        """
        Simulates a long-running operation by sleeping for 5 seconds.
        """
        logging.info("Simulating a long operation...")
        time.sleep(5)

    manager = LoadingManager(long_running_task)
    manager.execute()

    sys.exit(app.exec_())
