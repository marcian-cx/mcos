# mcos/ui/widgets/sidebar.py
from PyQt6.QtWidgets import QWidget, QTreeView, QVBoxLayout, QInputDialog, QMessageBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QKeySequence, QAction
from PyQt6.QtCore import Qt, QModelIndex
import os

MD_FILTER = (".md", ".markdown")

class Sidebar(QWidget):
    def __init__(self, vault_path: str, on_open):
        super().__init__()
        self.vault_path = os.path.abspath(vault_path)
        self.on_open = on_open

        self.view = QTreeView()
        self.view.setHeaderHidden(True)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Vault"])
        self.view.setModel(self.model)
        
        # E-ink optimized monospace styling
        self.view.setStyleSheet("""
        QTreeView {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 12px;
            border: none;
            outline: none;
            selection-background-color: #333333;
            selection-color: #ffffff;
            show-decoration-selected: 0;
        }
        QTreeView::item {
            padding: 2px;
            border: none;
            margin: 0px;
        }
        QTreeView::item:selected {
            background-color: #333333;
            color: #ffffff;
        }
        QTreeView::item:hover {
            background-color: #222222;
        }
        QTreeView::branch {
            background-color: #000000;
        }
        QTreeView::branch:has-children:closed:before {
            content: ">";
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
        }
        QTreeView::branch:has-children:open:before {
            content: "v";
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
        }
        """)

        self._populate()

        self.view.doubleClicked.connect(self._open)
        self.view.activated.connect(self._open)  # Triggered by Enter key
        
        # Override keyPressEvent to handle Enter manually
        original_keypress = self.view.keyPressEvent
        def keypress_handler(event):
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                current = self.view.currentIndex()
                if current.isValid():
                    self._open(current)
                return
            elif event.key() == Qt.Key.Key_N:
                self._new_file()
                return
            elif event.key() == Qt.Key.Key_D:
                self._delete_file()
                return
            original_keypress(event)
        self.view.keyPressEvent = keypress_handler
        
        # Keyboard shortcuts will be added by the main window
        
        lay = QVBoxLayout(self)
        lay.addWidget(self.view)

    def _add_dir(self, parent_item: QStandardItem, path: str):
        # Add directory node with terminal-style folder prefix
        dir_name = os.path.basename(path) or path
        dir_item = QStandardItem(f"/{dir_name}")
        dir_item.setEditable(False)
        dir_item.setData(path, Qt.ItemDataRole.UserRole)
        dir_item.setData("directory", Qt.ItemDataRole.UserRole + 1)  # Store type
        parent_item.appendRow(dir_item)

        # First add subdirectories, then md files (sorted)
        try:
            entries = sorted(os.listdir(path), key=str.lower)
        except PermissionError:
            return

        # Directories
        for name in entries:
            full = os.path.join(path, name)
            if os.path.isdir(full) and not name.startswith('.'):
                self._add_dir(dir_item, full)

        # Markdown files
        for name in entries:
            full = os.path.join(path, name)
            if os.path.isfile(full) and name.lower().endswith(MD_FILTER):
                file_item = QStandardItem(f"  {name}")
                file_item.setEditable(False)
                file_item.setData(full, Qt.ItemDataRole.UserRole)
                file_item.setData("file", Qt.ItemDataRole.UserRole + 1)  # Store type
                dir_item.appendRow(file_item)

    def _populate(self):
        self.model.removeRows(0, self.model.rowCount())
        root = QStandardItem(f"/{os.path.basename(self.vault_path)}")
        root.setEditable(False)
        root.setData(self.vault_path, Qt.ItemDataRole.UserRole)
        root.setData("directory", Qt.ItemDataRole.UserRole + 1)
        self.model.appendRow(root)
        self._add_dir(root, self.vault_path)
        self.view.expand(self.model.indexFromItem(root))

    def _open(self, ix: QModelIndex):
        item = self.model.itemFromIndex(ix)
        if not item:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        if path and os.path.isfile(path):
            self.on_open(path)
    
    def _new_file(self):
        """Create a new file in the selected directory"""
        current = self.view.currentIndex()
        if not current.isValid():
            return
            
        item = self.model.itemFromIndex(current)
        if not item:
            return
            
        item_type = item.data(Qt.ItemDataRole.UserRole + 1)
        path = item.data(Qt.ItemDataRole.UserRole)
        
        # Get directory path
        if item_type == "file":
            dir_path = os.path.dirname(path)
        else:  # directory
            dir_path = path
            
        # Ask for filename
        filename, ok = QInputDialog.getText(
            self, 
            "New File", 
            "Enter filename (without .md extension):",
            text=""
        )
        
        if not ok or not filename.strip():
            return
            
        # Ensure .md extension
        if not filename.endswith('.md'):
            filename += '.md'
            
        file_path = os.path.join(dir_path, filename)
        
        # Check if file already exists
        if os.path.exists(file_path):
            QMessageBox.warning(self, "File Exists", f"File '{filename}' already exists!")
            return
            
        # Create the file
        try:
            with open(file_path, 'w') as f:
                f.write(f"# {filename[:-3]}\n\n")  # Write title without .md
            
            # Refresh the tree
            self._populate()
            
            # Open the new file
            self.on_open(file_path)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create file: {str(e)}")
    
    def _delete_file(self):
        """Delete the selected file"""
        current = self.view.currentIndex()
        if not current.isValid():
            return
            
        item = self.model.itemFromIndex(current)
        if not item:
            return
            
        item_type = item.data(Qt.ItemDataRole.UserRole + 1)
        path = item.data(Qt.ItemDataRole.UserRole)
        
        # Only allow deleting files, not directories
        if item_type != "file":
            QMessageBox.warning(self, "Cannot Delete", "Can only delete files, not directories!")
            return
            
        filename = os.path.basename(path)
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Delete File",
            f"Are you sure you want to delete '{filename}'?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(path)
                # Refresh the tree
                self._populate()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete file: {str(e)}")