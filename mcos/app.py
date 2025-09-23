import sys, argparse
from PyQt6.QtWidgets import QApplication
from mcos.ui.main_window import MainWindow

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--vault", required=True, help="Path to vault root")
    return p.parse_args()

def main():
    args = parse_args()
    app = QApplication(sys.argv)
    win = MainWindow(args.vault)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()