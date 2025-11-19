# mcos/ui/widgets/csv_editor.py
import csv
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QPushButton, QLabel,
                             QStackedWidget, QPlainTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QAction, QKeySequence

class CSVEditor(QWidget):
    file_changed = pyqtSignal(str)
    modified_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.path = None
        self.modified = False
        self.is_table_view = True  # Track current view mode
        
        # Create table widget
        self.table = QTableWidget()
        self.table.setSortingEnabled(False)  # Disable sorting to preserve order
        
        # Make headers editable by double-clicking or pressing up from first row
        self.table.horizontalHeader().sectionDoubleClicked.connect(self._edit_column_header)
        
        # Create raw text editor
        self.text_editor = QPlainTextEdit()
        font = QFont("Monaco", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.text_editor.setFont(font)
        
        # Create stacked widget to switch between views
        self.stack = QStackedWidget()
        self.stack.addWidget(self.table)      # Index 0: Table view
        self.stack.addWidget(self.text_editor) # Index 1: Raw text view
        
        # E-ink optimized styling to match MCOS theme
        self.table.setStyleSheet("""
        QTableWidget {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 11px;
            border: none;
            gridline-color: #333333;
            selection-background-color: #333333;
            selection-color: #ffffff;
        }
        QTableWidget::item {
            padding: 4px;
            border: none;
        }
        QTableWidget::item:selected {
            background-color: #333333;
            color: #ffffff;
        }
        QHeaderView::section {
            background-color: #111111;
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 11px;
            font-weight: bold;
            padding: 4px;
            border: 1px solid #333333;
        }
        """)
        
        # Style text editor to match MCOS theme
        self.text_editor.setStyleSheet("""
        QPlainTextEdit {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 11px;
            border: none;
            selection-background-color: #333333;
            selection-color: #ffffff;
        }
        """)
        
        # Main layout - clean, no buttons
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)
        
        # Connect signals
        self.table.itemChanged.connect(self._on_item_changed)
        self.text_editor.textChanged.connect(self._on_text_changed)
        
        # Override table's key press event for smart navigation
        self.table.keyPressEvent = self._handle_key_press
        
        # Add keyboard shortcut for toggle
        self.setup_toggle_shortcut()
    
    def load_file(self, path: str):
        """Load CSV file into the table"""
        self.path = path
        
        try:
            with open(path, 'r', encoding='utf-8', newline='') as file:
                # Detect delimiter
                sample = file.read(1024)
                file.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                # Read CSV
                reader = csv.reader(file, delimiter=delimiter)
                data = list(reader)
                
                if not data:
                    return
                
                # Set up table
                headers = data[0]
                rows = data[1:]
                
                self.table.setRowCount(len(rows))
                self.table.setColumnCount(len(headers))
                self.table.setHorizontalHeaderLabels(headers)
                
                # Populate data
                for row_idx, row_data in enumerate(rows):
                    for col_idx, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(str(cell_data))
                        self.table.setItem(row_idx, col_idx, item)
                
                # Auto-resize columns to content
                self.table.resizeColumnsToContents()
                
                # Set minimum column widths for readability
                for col in range(self.table.columnCount()):
                    current_width = self.table.columnWidth(col)
                    min_width = 80  # Minimum width
                    max_width = 200  # Maximum width for very long content
                    self.table.setColumnWidth(col, max(min_width, min(current_width, max_width)))
                
                # Also load raw text for toggle functionality
                with open(path, 'r', encoding='utf-8') as f:
                    raw_content = f.read()
                    self.text_editor.setPlainText(raw_content)
                
                self.modified = False
                self.file_changed.emit(path)
                
        except Exception as e:
            print(f"Error loading CSV file: {e}")
    
    def save(self):
        """Save the CSV data back to file"""
        if not self.path:
            return
        
        try:
            if self.is_table_view:
                # Save from table view
                with open(self.path, 'w', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    
                    # Write headers
                    headers = []
                    for col in range(self.table.columnCount()):
                        header_item = self.table.horizontalHeaderItem(col)
                        header_text = header_item.text() if header_item else f"Column{col + 1}"
                        headers.append(header_text)
                    writer.writerow(headers)
                    
                    # Write data rows
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)
                            cell_data = item.text() if item else ""
                            row_data.append(cell_data)
                        writer.writerow(row_data)
            else:
                # Save from raw text view
                with open(self.path, 'w', encoding='utf-8') as file:
                    file.write(self.text_editor.toPlainText())
            
            self.modified = False
            self.modified_changed.emit()
                
        except Exception as e:
            print(f"Error saving CSV file: {e}")
    
    def _on_item_changed(self, item):
        """Handle when a cell is edited"""
        if not self.modified:
            self.modified = True
            self.modified_changed.emit()
    
    def _on_text_changed(self):
        """Handle when raw text is edited"""
        if not self.modified:
            self.modified = True
            self.modified_changed.emit()
    
    def setup_toggle_shortcut(self):
        """Setup keyboard shortcut for view toggle"""
        toggle_action = QAction("Toggle CSV View", self)
        toggle_action.setShortcut(QKeySequence("Ctrl+Shift+V"))
        toggle_action.triggered.connect(self.toggle_view)
        self.addAction(toggle_action)
    
    def toggle_view(self):
        """Toggle between table and raw text view"""
        if self.is_table_view:
            # Switch to raw text view
            self._sync_table_to_text()
            self.stack.setCurrentIndex(1)
            self.is_table_view = False
        else:
            # Switch to table view
            self._sync_text_to_table()
            self.stack.setCurrentIndex(0)
            self.is_table_view = True
    
    def _sync_table_to_text(self):
        """Convert table data to raw CSV text"""
        if not self.path:
            return
        
        lines = []
        
        # Add headers
        headers = []
        for col in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(col)
            header_text = header_item.text() if header_item else f"Column{col + 1}"
            headers.append(header_text)
        
        # Convert to CSV format
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        
        # Add data rows
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                cell_data = item.text() if item else ""
                row_data.append(cell_data)
            writer.writerow(row_data)
        
        # Set text editor content
        self.text_editor.setPlainText(output.getvalue())
    
    def _sync_text_to_table(self):
        """Convert raw CSV text to table data"""
        try:
            text_content = self.text_editor.toPlainText()
            
            # Parse CSV from text
            import io
            input_stream = io.StringIO(text_content)
            reader = csv.reader(input_stream)
            data = list(reader)
            
            if not data:
                return
            
            # Clear and rebuild table
            self.table.clear()
            
            headers = data[0]
            rows = data[1:] if len(data) > 1 else []
            
            self.table.setRowCount(len(rows))
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            
            # Populate data
            for row_idx, row_data in enumerate(rows):
                for col_idx, cell_data in enumerate(row_data):
                    if col_idx < len(headers):  # Ensure we don't exceed column count
                        item = QTableWidgetItem(str(cell_data))
                        self.table.setItem(row_idx, col_idx, item)
            
            # Auto-resize columns
            self.table.resizeColumnsToContents()
            for col in range(self.table.columnCount()):
                current_width = self.table.columnWidth(col)
                min_width = 80
                max_width = 200
                self.table.setColumnWidth(col, max(min_width, min(current_width, max_width)))
                
        except Exception as e:
            print(f"Error parsing CSV text: {e}")
    
    
    def _handle_key_press(self, event):
        """Handle key press events for smart navigation"""
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QTableWidget
        
        current_row = self.table.currentRow()
        current_col = self.table.currentColumn()
        
        # Handle arrow keys for smart expansion
        if event.key() == Qt.Key.Key_Right:
            # If we're in the last column, add a new column
            if current_col == self.table.columnCount() - 1:
                self._smart_add_column()
                # Move to the new column
                self.table.setCurrentCell(current_row, current_col + 1)
                return
        
        elif event.key() == Qt.Key.Key_Down:
            # If we're in the last row, add a new row
            if current_row == self.table.rowCount() - 1:
                self._smart_add_row()
                # Move to the new row
                self.table.setCurrentCell(current_row + 1, current_col)
                return
        
        elif event.key() == Qt.Key.Key_Left:
            # Check if we're leaving an empty column that we can delete
            if current_col > 0:  # Don't delete if moving to first column
                self._check_and_delete_empty_column(current_col)
        
        elif event.key() == Qt.Key.Key_Up:
            # If we're in the first row, allow editing the column header
            if current_row == 0:
                self._edit_column_header(current_col)
                return
            # Check if we're leaving an empty row that we can delete
            elif current_row > 0:
                self._check_and_delete_empty_row(current_row)
        
        # Call the original key press handler for default behavior
        QTableWidget.keyPressEvent(self.table, event)
    
    def _smart_add_column(self):
        """Add a new column intelligently"""
        col_count = self.table.columnCount()
        self.table.insertColumn(col_count)
        
        # Set header for new column
        header_item = QTableWidgetItem(f"Column{col_count + 1}")
        self.table.setHorizontalHeaderItem(col_count, header_item)
        
        # Add empty items to all rows in the new column
        for row in range(self.table.rowCount()):
            item = QTableWidgetItem("")
            self.table.setItem(row, col_count, item)
        
        self._on_item_changed(None)  # Mark as modified
    
    def _smart_add_row(self):
        """Add a new row intelligently"""
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        
        # Add empty items to the new row
        for col in range(self.table.columnCount()):
            item = QTableWidgetItem("")
            self.table.setItem(row_count, col, item)
        
        self._on_item_changed(None)  # Mark as modified
    
    def _check_and_delete_empty_column(self, col_index):
        """Delete column if it's empty and we're moving away from it"""
        if self.table.columnCount() <= 1:  # Keep at least one column
            return
        
        # Check if the column is completely empty
        is_empty = True
        for row in range(self.table.rowCount()):
            item = self.table.item(row, col_index)
            if item and item.text().strip():
                is_empty = False
                break
        
        if is_empty:
            self.table.removeColumn(col_index)
            self._on_item_changed(None)  # Mark as modified
    
    def _check_and_delete_empty_row(self, row_index):
        """Delete row if it's empty and we're moving away from it"""
        if self.table.rowCount() <= 1:  # Keep at least one row
            return
        
        # Check if the row is completely empty
        is_empty = True
        for col in range(self.table.columnCount()):
            item = self.table.item(row_index, col)
            if item and item.text().strip():
                is_empty = False
                break
        
        if is_empty:
            self.table.removeRow(row_index)
            self._on_item_changed(None)  # Mark as modified
    
    def _edit_column_header(self, logical_index):
        """Allow editing of column headers by double-clicking"""
        from PyQt6.QtWidgets import QInputDialog
        
        current_header = self.table.horizontalHeaderItem(logical_index)
        current_text = current_header.text() if current_header else f"Column{logical_index + 1}"
        
        # Show input dialog to edit header
        new_text, ok = QInputDialog.getText(
            self, 
            "Edit Column Header", 
            "Column name:", 
            text=current_text
        )
        
        if ok and new_text.strip():
            # Update the header
            header_item = QTableWidgetItem(new_text.strip())
            self.table.setHorizontalHeaderItem(logical_index, header_item)
            self._on_item_changed(None)  # Mark as modified
