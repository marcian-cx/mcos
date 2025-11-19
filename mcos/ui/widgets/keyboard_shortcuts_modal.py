from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class KeyboardShortcutsModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keyboard Shortcuts")
        self.setModal(True)
        self.resize(600, 500)

        # E-ink optimized dark theme with monospace
        self.setStyleSheet("""
        QDialog {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 12px;
            border: 1px solid #333333;
        }
        QLabel {
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 12px;
        }
        QTextEdit {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 11px;
            border: none;
            padding: 8px;
            selection-background-color: #333333;
            selection-color: #ffffff;
        }
        QPushButton {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #666666;
            padding: 8px 16px;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #444444;
        }
        """)

        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Keyboard Shortcuts")
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(title)

        # Shortcuts text area
        self.shortcuts_text = QTextEdit()
        self.shortcuts_text.setReadOnly(True)
        self._populate_shortcuts()
        layout.addWidget(self.shortcuts_text)

        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        # Set focus to close button for easy dismissal
        close_button.setFocus()

    def _populate_shortcuts(self):
        shortcuts = """
GENERAL
  Ctrl+S          Save current file
  Ctrl+Left       Focus sidebar
  Ctrl+Right      Focus editor
  Ctrl+K          Show keyboard shortcuts

SIDEBAR (File Management)
  Enter           Open selected file
  Ctrl+N          Create new markdown file
  Ctrl+Shift+N    Create new CSV file
  Ctrl+D          Delete selected file
  Ctrl+R          Rename selected file

EDITOR (Markdown)
  Ctrl+T          Toggle task checkbox (- [ ] ↔ - [x])
  Tab             Indent line/block
  Shift+Tab       Dedent line/block
  Enter           Continue task list or normal line break

EDITOR (CSV)
  Ctrl+Shift+V    Toggle between table and raw CSV view
  Tab             Move to next cell
  Shift+Tab       Move to previous cell
  Enter           Move to next row
  Ctrl+S          Save CSV file
        """

        self.shortcuts_text.setPlainText(shortcuts.strip())
