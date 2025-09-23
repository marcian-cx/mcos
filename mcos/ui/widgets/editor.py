from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QStackedWidget, QLabel
from PyQt6.QtGui import QFont, QAction, QKeySequence
from PyQt6.QtCore import pyqtSignal, Qt
from .markdown_viewer import MarkdownViewer
from ...core.tasks import parse_task_line
import os, time, re

class Editor(QWidget):
    file_changed = pyqtSignal()
    modified_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.path = None
        self.modified = False
        self.is_preview_mode = False
        
        self.edit = QPlainTextEdit()
        font = QFont("Monaco", 12)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.edit.setFont(font)
        self.edit.textChanged.connect(self._mark_dirty)
        
        # E-ink optimized monospace styling  
        self.edit.setStyleSheet("""
        QPlainTextEdit {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 12px;
            border: none;
            padding: 8px;
            line-height: 1.4;
            selection-background-color: #333333;
            selection-color: #ffffff;
        }
        """)
        
        # Override keyPressEvent for task toggling
        original_keypress = self.edit.keyPressEvent
        def keypress_handler(event):
            if event.key() == Qt.Key.Key_Space and not self.is_preview_mode:
                if self._try_toggle_task():
                    return
            original_keypress(event)
        self.edit.keyPressEvent = keypress_handler
        
        self.viewer = MarkdownViewer()
        
        # Add filename label at the top
        self.filename_label = QLabel("No file open")
        self.filename_label.setStyleSheet("""
        QLabel {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 11px;
            padding: 4px 8px;
            border-bottom: 1px solid #333333;
        }
        """)
        
        self.stack = QStackedWidget()
        self.stack.addWidget(self.edit)
        self.stack.addWidget(self.viewer)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(self.filename_label)
        lay.addWidget(self.stack)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save)
        self.addAction(save_action)
        
        toggle_action = QAction("Toggle Preview", self)
        toggle_action.setShortcut(QKeySequence("F5"))
        toggle_action.triggered.connect(self.toggle_preview)
        self.addAction(toggle_action)

    def load_file(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            self.edit.setPlainText(f.read())
        self.path = path
        self.modified = False
        
        # Update filename label with terminal-style formatting
        filename = os.path.basename(path)
        self.filename_label.setText(f"<< {filename}")
        
        self.file_changed.emit()
        self.modified_changed.emit()

    def save(self):
        if not self.path: return
        text = self.edit.toPlainText()
        tmp = f"{self.path}.~{int(time.time())}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, self.path)
        self.modified = False
        self.modified_changed.emit()

    def toggle_preview(self):
        self.is_preview_mode = not self.is_preview_mode
        
        if self.is_preview_mode:
            text = self.edit.toPlainText()
            self.viewer.set_markdown(text)
            self.stack.setCurrentWidget(self.viewer)
        else:
            self.stack.setCurrentWidget(self.edit)
            self.edit.setFocus()

    def _try_toggle_task(self) -> bool:
        cursor = self.edit.textCursor()
        cursor.select(cursor.SelectionType.LineUnderCursor)
        line_text = cursor.selectedText()
        
        # Check if this line is a task
        task_match = re.match(r'^(\s*)- \[([ x])\] (.+)$', line_text)
        if not task_match:
            return False
        
        indent, status, content = task_match.groups()
        new_status = 'x' if status == ' ' else ' '
        new_line = f"{indent}- [{new_status}] {content}"
        
        # Replace the line
        cursor.removeSelectedText()
        cursor.insertText(new_line)
        return True

    def _mark_dirty(self):
        was_modified = self.modified
        self.modified = True
        if not was_modified:
            self.modified_changed.emit()