#!/usr/bin/env python3
"""
MCOS Launcher - Mission Command OS
Launches MCOS with default vault in home directory
"""

import sys
import os
import json
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog
from mcos.ui.main_window import MainWindow

def get_config_file():
    """Get path to MCOS config file"""
    return Path.home() / ".mcos_config.json"

def load_last_vault():
    """Load the last used vault from config"""
    config_file = get_config_file()
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('last_vault')
        except:
            pass
    return None

def save_vault_location(vault_path):
    """Save vault location to config"""
    config_file = get_config_file()
    config = {'last_vault': vault_path}
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f)
    except:
        pass

def find_vault():
    """Find or create MCOS vault directory"""
    # First check last used vault
    last_vault = load_last_vault()
    if last_vault and Path(last_vault).exists():
        return last_vault
    
    # Check for vault in home directory
    home_vault = Path.home() / "mcos_vault"
    if home_vault.exists():
        vault_path = str(home_vault)
        save_vault_location(vault_path)
        return vault_path
    
    # Check for demo vault in current directory
    demo_vault = Path("demo_vault")
    if demo_vault.exists():
        vault_path = str(demo_vault.absolute())
        save_vault_location(vault_path)
        return vault_path
    
    # Ask user to select vault location
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setWindowTitle("MCOS - Select Vault")
    msg.setText("No MCOS vault found. Please select a directory to use as your vault.")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()
    
    vault_dir = QFileDialog.getExistingDirectory(
        None, 
        "Select MCOS Vault Directory",
        str(Path.home())
    )
    
    if not vault_dir:
        sys.exit(1)
    
    save_vault_location(vault_dir)
    return vault_dir

def main():
    """Launch MCOS"""
    try:
        vault_path = find_vault()
        
        app = QApplication(sys.argv)
        app.setApplicationName("MCOS")
        app.setApplicationDisplayName("Mission Command OS")
        
        # Set dark theme for the entire app
        app.setStyle("Fusion")
        
        window = MainWindow(vault_path)
        window.show()
        
        sys.exit(app.exec())
        
    except Exception as e:
        app = QApplication(sys.argv)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("MCOS Error")
        msg.setText(f"Failed to launch MCOS:\n{str(e)}")
        msg.exec()
        sys.exit(1)

if __name__ == "__main__":
    main()
