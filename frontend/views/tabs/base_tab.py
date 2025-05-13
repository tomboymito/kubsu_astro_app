from PyQt5.QtWidgets import QWidget

class BaseTab(QWidget):
    def __init__(self, title=""):
        super().__init__()
        self.title = title
        self.init_ui()
        
    def init_ui(self):
        pass