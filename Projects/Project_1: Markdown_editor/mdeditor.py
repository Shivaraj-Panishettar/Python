import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit,
    QFileDialog, QAction, QSplitter, QListWidget, QMessageBox, QStackedWidget, QTabWidget, QTabBar
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QIcon
import markdown
import json

# MathJax and Syntax Highlighting for code
import markdown.extensions.fenced_code

class WelcomeScreen(QWidget):
    def __init__(self, enter_editor_callback):
        super().__init__()
        self.enter_editor_callback = enter_editor_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("📝 Markdown Manager")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")

        subtitle = QLabel("Organize and Edit Your Markdown Files with Live Preview")
        subtitle.setStyleSheet("font-size: 16px; color: #666; margin-bottom: 20px;")

        button = QPushButton("Open Editor")
        button.setFixedSize(200, 40)
        button.clicked.connect(self.enter_editor_callback)
        button.setStyleSheet("""
            QPushButton {
                font-size: 16px; padding: 10px;
                background-color: #3498db; color: white; border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(button)
        self.setLayout(layout)


class MarkdownEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.current_file_path = None
        self.file_paths = []
        self.preview_fullscreen = False
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.init_ui()

    def init_ui(self):
        self.file_list = QListWidget()
        self.file_list.setFixedWidth(250)
        self.file_list.itemClicked.connect(self.load_selected_file)
        self.file_list.setStyleSheet("padding: 5px; font-size: 14px;")

        self.editor = QTextEdit()
        self.editor.textChanged.connect(self.update_preview)
        self.editor.setStyleSheet("padding: 10px; font-size: 14px;")

        self.preview = QWebEngineView()

        editor_splitter = QSplitter(Qt.Vertical)
        editor_splitter.addWidget(self.editor)
        editor_splitter.addWidget(self.preview)
        editor_splitter.setSizes([500, 500])

        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.file_list)
        main_splitter.addWidget(editor_splitter)
        main_splitter.setSizes([250, 950])

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addWidget(main_splitter)
        self.setLayout(layout)

    def load_selected_file(self, item):
        selected_filename = item.text()
        for path in self.file_paths:
            if path.endswith(selected_filename):
                self.load_file(path)
                break

    def update_preview(self):
        raw_markdown = self.editor.toPlainText()
        html = markdown.markdown(raw_markdown, extensions=['fenced_code', 'mathjax'])
        self.preview.setHtml(html)

    def load_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                tab = self.create_tab(path, content)
                self.tabs.addTab(tab, os.path.basename(path))
                self.current_file_path = path
                self.update_preview()
                self.refresh_file_list(os.path.dirname(path))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load file:\n{e}")

    def refresh_file_list(self, folder=None):
        if folder:
            self.file_list.clear()
            self.file_paths = []
            for file in os.listdir(folder):
                if file.endswith(".md"):
                    full_path = os.path.join(folder, file)
                    self.file_paths.append(full_path)
                    self.file_list.addItem(file)

    def new_file(self):
        self.editor.clear()
        self.preview.setHtml("")
        self.current_file_path = None

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Markdown File", "", "Markdown Files (*.md)")
        if path:
            self.load_file(path)

    def save_file(self):
        if self.current_file_path:
            with open(self.current_file_path, "w", encoding="utf-8") as file:
                file.write(self.editor.toPlainText())
        else:
            self.save_file_as()

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Markdown File", "", "Markdown Files (*.md)")
        if path:
            self.current_file_path = path
            self.save_file()

    def remove_file(self):
        if self.current_file_path:
            confirm = QMessageBox.question(self, "Remove File",
                                           f"Delete '{os.path.basename(self.current_file_path)}'?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                try:
                    os.remove(self.current_file_path)
                    self.editor.clear()
                    self.preview.setHtml("")
                    self.current_file_path = None
                    self.refresh_file_list()
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

    def close_tab(self, index):
        tab_widget = self.tabs.widget(index)
        self.tabs.removeTab(index)
        tab_widget.deleteLater()

    def toggle_preview_fullscreen(self):
        if not self.preview_fullscreen:
            self.preview.showFullScreen()
        else:
            self.preview.showNormal()
        self.preview_fullscreen = not self.preview_fullscreen

    def create_tab(self, path, content):
        editor_widget = QWidget()
        layout = QVBoxLayout()

        editor = QTextEdit()
        editor.setText(content)
        editor.setStyleSheet("padding: 10px; font-size: 14px;")

        preview = QWebEngineView()
        preview.setStyleSheet("background-color: #fff; padding: 10px;")
        html_content = markdown.markdown(content, extensions=['fenced_code', 'mathjax'])
        preview.setHtml(html_content)

        layout.addWidget(editor)
        layout.addWidget(preview)
        editor_widget.setLayout(layout)
        return editor_widget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown File Manager")
        self.setGeometry(100, 100, 1200, 700)

        self.stack = QStackedWidget()
        self.editor_widget = MarkdownEditor()
        self.welcome_screen = WelcomeScreen(self.animate_to_editor)

        self.stack.addWidget(self.welcome_screen)
        self.stack.addWidget(self.editor_widget)

        self.setCentralWidget(self.stack)
        self.create_menu()

        self.dark_mode = False
        self.apply_theme()

    def animate_to_editor(self):
        self.stack.setCurrentWidget(self.editor_widget)
        anim = QPropertyAnimation(self.stack, b"geometry")
        anim.setDuration(500)
        anim.setStartValue(QRect(0, 0, self.width(), self.height()))
        anim.setEndValue(QRect(0, 0, self.width(), self.height()))
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        new_action = QAction(QIcon('icons/new.png'), "New", self)
        new_action.triggered.connect(self.editor_widget.new_file)
        file_menu.addAction(new_action)

        open_action = QAction(QIcon('icons/open.png'), "Open File", self)
        open_action.triggered.connect(self.editor_widget.open_file)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon('icons/save.png'), "Save", self)
        save_action.triggered.connect(self.editor_widget.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction(QIcon('icons/save_as.png'), "Save As...", self)
        save_as_action.triggered.connect(self.editor_widget.save_file_as)
        file_menu.addAction(save_as_action)

        remove_action = QAction(QIcon('icons/remove.png'), "Remove File", self)
        remove_action.triggered.connect(self.editor_widget.remove_file)
        file_menu.addAction(remove_action)

        view_menu = menubar.addMenu("View")

        fullscreen_action = QAction("Toggle Preview Fullscreen", self)
        fullscreen_action.triggered.connect(self.editor_widget.toggle_preview_fullscreen)
        view_menu.addAction(fullscreen_action)

        theme_action = QAction("Toggle Dark Mode", self)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            dark_stylesheet = """
                QMainWindow { background-color: #2b2b2b; color: white; }
                QTextEdit, QListWidget { background-color: #3c3f41; color: white; }
                QMenuBar, QMenu, QMenu::item:selected { background-color: #2b2b2b; color: white; }
                QPushButton { background-color: #555; color: white; }
            """
            self.setStyleSheet(dark_stylesheet)
        else:
            self.setStyleSheet("")  # Use default light theme


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

