from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLabel
from PyQt6.QtGui import QFont, QAction, QKeySequence
from PyQt6.QtCore import pyqtSignal, Qt
from ...core.tasks import parse_task_line
from ...services.markdown_editor_service import MarkdownEditorService
import os, time, re

class Editor(QWidget):
    file_changed = pyqtSignal()
    modified_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.path = None
        self.modified = False
        
        # Initialize the markdown service
        self.markdown_service = MarkdownEditorService()
        
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
        
        # Override keyPressEvent for enhanced markdown editing
        original_keypress = self.edit.keyPressEvent
        def keypress_handler(event):
            # Task toggle with Ctrl+T
            if event.key() == Qt.Key.Key_T and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                if self._handle_task_toggle():
                    return
            
            # Enter key for checkbox continuation
            elif event.key() == Qt.Key.Key_Return:
                if self._handle_enter_key():
                    return
            
            # Tab key for indentation
            elif event.key() == Qt.Key.Key_Tab:
                if self._handle_tab_key(False):  # False for indent
                    return
            
            # Shift+Tab for dedentation (Qt sends this as Backtab)
            elif event.key() == Qt.Key.Key_Backtab:
                if self._handle_tab_key(True):  # True for dedent
                    return
            
            # Default behavior for other keys
            original_keypress(event)
        
        self.edit.keyPressEvent = keypress_handler
        
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
        
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(self.filename_label)
        lay.addWidget(self.edit)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save)
        self.addAction(save_action)
        

    def load_file(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            self.edit.setPlainText(content)
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

    def _handle_task_toggle(self) -> bool:
        """Handle Ctrl+T task toggle using the markdown service"""
        cursor = self.edit.textCursor()
        cursor.select(cursor.SelectionType.LineUnderCursor)
        line_text = cursor.selectedText()
        
        new_line = self.markdown_service.toggle_task_status(line_text)
        if new_line is None:
            return False
        
        # Replace the line
        cursor.removeSelectedText()
        cursor.insertText(new_line)
        return True
    
    def _handle_enter_key(self) -> bool:
        """Handle Enter key for checkbox continuation"""
        cursor = self.edit.textCursor()
        cursor.select(cursor.SelectionType.LineUnderCursor)
        current_line = cursor.selectedText()
        
        new_line = self.markdown_service.handle_enter_key(current_line)
        if new_line is None:
            return False
        
        # Move to end of line and insert new line
        cursor.movePosition(cursor.MoveOperation.EndOfLine)
        self.edit.setTextCursor(cursor)
        self.edit.insertPlainText(f"\n{new_line}")
        return True
    
    def _handle_tab_key(self, is_dedent: bool) -> bool:
        """Handle Tab/Shift+Tab for indentation"""
        cursor = self.edit.textCursor()
        
        # If there's a selection, handle multiple lines
        if cursor.hasSelection():
            return self._handle_tab_selection(cursor, is_dedent)
        
        # Handle single line
        cursor.select(cursor.SelectionType.LineUnderCursor)
        line_text = cursor.selectedText()
        
        new_line = self.markdown_service.handle_tab_key(line_text, is_dedent)
        
        # Replace the line
        cursor.removeSelectedText()
        cursor.insertText(new_line)
        return True
    
    def _handle_tab_selection(self, cursor, is_dedent: bool) -> bool:
        """Handle Tab/Shift+Tab for multiple selected lines"""
        # Get the selection
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        
        # Move to start of selection and select full lines
        cursor.setPosition(start)
        cursor.movePosition(cursor.MoveOperation.StartOfLine)
        start_pos = cursor.position()
        
        cursor.setPosition(end)
        cursor.movePosition(cursor.MoveOperation.EndOfLine)
        end_pos = cursor.position()
        
        # Select the full lines
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, cursor.MoveMode.KeepAnchor)
        
        selected_text = cursor.selectedText()
        lines = selected_text.split('\n')
        
        # Process each line
        new_lines = []
        for line in lines:
            new_line = self.markdown_service.handle_tab_key(line, is_dedent)
            new_lines.append(new_line)
        
        # Replace the selection
        cursor.removeSelectedText()
        cursor.insertText('\n'.join(new_lines))
        
        return True

    def _mark_dirty(self):
        was_modified = self.modified
        self.modified = True
        if not was_modified:
            self.modified_changed.emit()