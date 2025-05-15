from app.frontend.front_v2 import MainApplication
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())
