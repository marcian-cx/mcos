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
            background: transparent;
            border: none;
            width: 0px;
            height: 0px;
        }
        """)

        self._populate()

        self.view.doubleClicked.connect(self._open)
        self.view.activated.connect(self._open)  # Triggered by Enter key
        self.view.expanded.connect(self._on_expanded)
        self.view.collapsed.connect(self._on_collapsed)
        
        # Override keyPressEvent to handle Enter manually
        original_keypress = self.view.keyPressEvent
        def keypress_handler(event):
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                current = self.view.currentIndex()
                if current.isValid():
                    self._open(current)
                return
            elif event.key() == Qt.Key.Key_N and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self._new_file()
                return
            elif event.key() == Qt.Key.Key_D and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self._delete_file()
                return
            elif event.key() == Qt.Key.Key_R and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self._rename_file()
                return
            original_keypress(event)
        self.view.keyPressEvent = keypress_handler
        
        # Keyboard shortcuts will be added by the main window
        
        lay = QVBoxLayout(self)
        lay.addWidget(self.view)

    def _add_dir(self, parent_item: QStandardItem, path: str):
        # Add directory node with simple caret - no prefix lines
        dir_name = os.path.basename(path) or path
        dir_item = QStandardItem(f"▶ {dir_name}")
        dir_item.setEditable(False)
        dir_item.setData(path, Qt.ItemDataRole.UserRole)
        dir_item.setData("directory", Qt.ItemDataRole.UserRole + 1)
        parent_item.appendRow(dir_item)

        # Get all entries
        try:
            entries = sorted(os.listdir(path), key=str.lower)
        except PermissionError:
            return

        # Separate directories and files
        dirs = [e for e in entries if os.path.isdir(os.path.join(path, e)) and not e.startswith('.')]
        files = [e for e in entries if os.path.isfile(os.path.join(path, e)) and e.lower().endswith(MD_FILTER)]
        
        # Add directories
        for name in dirs:
            full = os.path.join(path, name)
            self._add_dir(dir_item, full)

        # Add files
        for name in files:
            full = os.path.join(path, name)
            file_item = QStandardItem(f"  {name}")
            file_item.setEditable(False)
            file_item.setData(full, Qt.ItemDataRole.UserRole)
            file_item.setData("file", Qt.ItemDataRole.UserRole + 1)
            dir_item.appendRow(file_item)

    def _get_expanded_paths(self):
        """Get list of currently expanded directory paths"""
        expanded = []
        for i in range(self.model.rowCount()):
            self._collect_expanded_paths(self.model.item(i), expanded)
        return expanded
    
    def _collect_expanded_paths(self, item, expanded):
        """Recursively collect expanded directory paths"""
        if item:
            index = self.model.indexFromItem(item)
            if self.view.isExpanded(index):
                item_type = item.data(Qt.ItemDataRole.UserRole + 1)
                if item_type == "directory":
                    path = item.data(Qt.ItemDataRole.UserRole)
                    expanded.append(path)
            
            for i in range(item.rowCount()):
                self._collect_expanded_paths(item.child(i), expanded)
    
    def _restore_expanded_paths(self, expanded_paths):
        """Restore expanded state for directories"""
        for i in range(self.model.rowCount()):
            self._expand_matching_paths(self.model.item(i), expanded_paths)
    
    def _expand_matching_paths(self, item, expanded_paths):
        """Recursively expand directories that were previously expanded"""
        if item:
            item_type = item.data(Qt.ItemDataRole.UserRole + 1)
            if item_type == "directory":
                path = item.data(Qt.ItemDataRole.UserRole)
                if path in expanded_paths:
                    index = self.model.indexFromItem(item)
                    self.view.expand(index)
            
            for i in range(item.rowCount()):
                self._expand_matching_paths(item.child(i), expanded_paths)

    def _populate(self):
        # Save current expanded state
        expanded_paths = self._get_expanded_paths()
        
        self.model.removeRows(0, self.model.rowCount())
        root = QStandardItem(f"▼ {os.path.basename(self.vault_path)}")
        root.setEditable(False)
        root.setData(self.vault_path, Qt.ItemDataRole.UserRole)
        root.setData("directory", Qt.ItemDataRole.UserRole + 1)
        self.model.appendRow(root)
        
        # Populate root directory contents
        try:
            entries = sorted(os.listdir(self.vault_path), key=str.lower)
            dirs = [e for e in entries if os.path.isdir(os.path.join(self.vault_path, e)) and not e.startswith('.')]
            files = [e for e in entries if os.path.isfile(os.path.join(self.vault_path, e)) and e.lower().endswith(MD_FILTER)]
            
            # Add directories
            for name in dirs:
                full = os.path.join(self.vault_path, name)
                self._add_dir(root, full)

            # Add files
            for name in files:
                full = os.path.join(self.vault_path, name)
                file_item = QStandardItem(f"  {name}")
                file_item.setEditable(False)
                file_item.setData(full, Qt.ItemDataRole.UserRole)
                file_item.setData("file", Qt.ItemDataRole.UserRole + 1)
                root.appendRow(file_item)
                
        except PermissionError:
            pass
        
        # Always expand root
        self.view.expand(self.model.indexFromItem(root))
        
        # Restore previously expanded directories
        self._restore_expanded_paths(expanded_paths)

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



    def _rename_file(self):
        """Rename the selected file"""
        current = self.view.currentIndex()
        if not current.isValid():
            return
            
        item = self.model.itemFromIndex(current)
        if not item:
            return
            
        item_type = item.data(Qt.ItemDataRole.UserRole + 1)
        old_path = item.data(Qt.ItemDataRole.UserRole)
        
        if item_type != "file":
            QMessageBox.warning(self, "Cannot Rename", "Can only rename files, not directories!")
            return
            
        old_filename = os.path.basename(old_path)
        name_without_ext = os.path.splitext(old_filename)[0]
        
        new_name, ok = QInputDialog.getText(
            self, 
            "Rename File", 
            "Enter new filename (without .md extension):", 
            text=name_without_ext
        )
        
        if not ok or not new_name.strip():
            return
            
        if not new_name.endswith('.md'):
            new_name += '.md'
            
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        
        if os.path.exists(new_path):
            QMessageBox.warning(self, "File Exists", f"File '{new_name}' already exists!")
            return
            
        try:
            os.rename(old_path, new_path)
            self._populate()
            # If the renamed file was open in editor, update it
            if hasattr(self, 'on_open') and callable(self.on_open):
                self.on_open(new_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to rename file: {str(e)}")

    def _on_expanded(self, index):
        """Handle directory expansion - change ▶ to ▼"""
        item = self.model.itemFromIndex(index)
        if item and item.data(Qt.ItemDataRole.UserRole + 1) == "directory":
            text = item.text()
            if "▶" in text:
                new_text = text.replace("▶", "▼")
                item.setText(new_text)

    def _on_collapsed(self, index):
        """Handle directory collapse - change ▼ to ▶"""
        item = self.model.itemFromIndex(index)
        if item and item.data(Qt.ItemDataRole.UserRole + 1) == "directory":
            text = item.text()
            if "▼" in text:
                new_text = text.replace("▼", "▶")
                item.setText(new_text)
            