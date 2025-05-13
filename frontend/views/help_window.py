from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt

class HelpWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справка")
        self.setFixedSize(900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(60, 60, 60, 60)
        
        outer_frame = QFrame()
        outer_frame.setFrameShape(QFrame.Box)
        outer_frame.setLineWidth(2)
        outer_frame.setStyleSheet("""background-color: #0b0b47;
        border-radius: 20px;     
        border: 2px solid white;
        """)
        layout.addWidget(outer_frame)
        
        inner_layout = QVBoxLayout(outer_frame)
        inner_layout.setContentsMargins(10, 10, 10, 10)
        
        content = QLabel("""Здесь будет справочная информация""")
        content.setStyleSheet("""background-color: #0b0b47;
        border-radius: 20px;      
        color: white;
        border: none;
        """)
        content.setAlignment(Qt.AlignCenter)
        inner_layout.addWidget(content, 1)
        
        self.close_btn = QPushButton("Спасибо!")
        self.close_btn.setFixedSize(750, 40)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: white;  
                border-radius: 20px;     
                color: #000034;   
                font-size: 20px;
                border: none;
                }
            QPushButton:hover {
                background-color: #aaccff;
                }
            """)
        self.close_btn.clicked.connect(self.close)
        inner_layout.addWidget(self.close_btn, 0, Qt.AlignBottom | Qt.AlignHCenter)