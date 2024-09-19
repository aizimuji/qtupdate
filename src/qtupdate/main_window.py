import os
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QMenuBar,
    QMenu,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import Qt
import requests
from bs4 import BeautifulSoup
from qtupdate.updater import check_for_updates
from qtupdate.version import __version__


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Crawler")
        self.setGeometry(100, 100, 800, 600)

        self.setup_ui()
        self.setup_menu()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.crawl_button = QPushButton("Crawl")
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.crawl_button)

        self.html_display = QTextEdit()
        self.html_display.setReadOnly(True)

        self.save_button = QPushButton("Save HTML")

        layout.addLayout(url_layout)
        layout.addWidget(self.html_display)
        layout.addWidget(self.save_button)

        self.crawl_button.clicked.connect(self.crawl_url)
        self.save_button.clicked.connect(self.save_html)

    def setup_menu(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")

        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)

        check_update_action = help_menu.addAction("Check for Updates")
        check_update_action.triggered.connect(self.check_for_updates)

    def crawl_url(self):
        url = self.url_input.text()
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            self.html_display.setPlainText(soup.prettify())
        except Exception as e:
            self.html_display.setPlainText(f"Error: {str(e)}")

    def save_html(self):
        html_content = self.html_display.toPlainText()
        if html_content:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save HTML File", "", "HTML Files (*.html)"
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                QMessageBox.information(
                    self, "Save Successful", f"HTML content saved to {file_path}"
                )
        else:
            QMessageBox.warning(self, "Save Failed", "No content to save")

    def show_about(self):
        version = ".".join(map(str, __version__))
        QMessageBox.information(self, "About", f"Web Crawler Demo\nVersion {version}")

    def check_for_updates(self):
        update_available, version = check_for_updates()
        if update_available:
            reply = QMessageBox.question(
                self,
                "Update Available",
                f"A new version ({version}) is available. Do you want to update?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.perform_update()
        else:
            QMessageBox.information(
                self, "No Updates", "You are using the latest version."
            )

    def perform_update(self):
        # Implement the update process here
        # This should download the new exe and replace the current one
        pass
