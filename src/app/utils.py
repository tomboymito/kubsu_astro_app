import sys
import os
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу, работает для dev и для PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def create_param_row(label_text, input_widget, label_style=""):
    row_widget = QWidget()
    row_layout = QHBoxLayout(row_widget)
    row_layout.setContentsMargins(0, 0, 0, 0)
    
    label = QLabel(label_text)
    if label_style:
        label.setStyleSheet(label_style)
    else:
        label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: white;
                min-width: 250px;
            }
        """)
    label.setWordWrap(True)
    
    input_widget.setMinimumHeight(30)
    input_widget.setStyleSheet("""
        QLineEdit {
            background-color: white;
            border-radius: 5px;
            color: #000034;
            padding: 5px;
            font-size: 14px;
        }
    """)
    
    row_layout.addWidget(label, 1)
    row_layout.addWidget(input_widget, 2)
    
    return row_widget