import sys
import os

if __name__ == "__main__":
    # Add the parent directory to sys.path to allow imports of frontend as a package
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from PyQt5.QtWidgets import QApplication
    from frontend.views.main_window import MainApplication

    app = QApplication(sys.argv)
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())
