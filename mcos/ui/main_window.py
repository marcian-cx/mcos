from PyQt6.QtWidgets import QMainWindow, QWidget, QSplitter, QVBoxLayout, QStatusBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence
from .widgets.sidebar import Sidebar
from .widgets.editor import Editor

class MainWindow(QMainWindow):
    def __init__(self, vault_path: str):
        super().__init__()
        self.setWindowTitle("MCOS")
        self.resize(1200, 800)
        
        # E-ink optimized dark theme with monospace
        self.setStyleSheet("""
        QMainWindow {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 12px;
        }
        QSplitter::handle {
            background-color: #333333;
            width: 1px;
            height: 1px;
        }
        QStatusBar {
            background-color: #000000;
            color: #ffffff;
            border-top: 1px solid #333333;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            padding: 2px;
        }
        """)

        self.editor = Editor()
        self.sidebar = Sidebar(vault_path, on_open=self.open_file)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        split = QSplitter(Qt.Orientation.Horizontal)
        split.addWidget(self.sidebar)
        split.addWidget(self.editor)
        split.setStretchFactor(0, 0)
        split.setStretchFactor(1, 1)

        root = QWidget()
        lay = QVBoxLayout(root)
        lay.addWidget(split)
        self.setCentralWidget(root)
        
        self.editor.file_changed.connect(self.update_status)
        self.editor.modified_changed.connect(self.update_status)
        

    def open_file(self, path: str):
        self.editor.load_file(path)
        self.update_status()
    
    def update_status(self):
        if self.editor.path:
            status = f"{self.editor.path}"
            if self.editor.modified:
                status += " *"
            self.status_bar.showMessage(status)
        else:
            self.status_bar.showMessage("Ready")