from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QComboBox, QPushButton, QFrame)
from PyQt5.QtWidgets import QListView
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from .base_tab import BaseTab

class GraphTab(BaseTab):
    def init_ui(self):
        self.setStyleSheet("background-color: #0b0b47;")
        layout = QVBoxLayout(self)
        
        self.init_graph_selector(layout)
        self.init_graph_canvas(layout)
        self.init_graph_controls(layout)

    def init_graph_selector(self, layout):
        graph_selector_layout = QHBoxLayout()
        graph_label = QLabel("Тип графика:")
        graph_label.setStyleSheet("""
            color: white; 
            font-weight: bold; 
            font-size: 16px;
        """)

        self.graph_combo = QComboBox()
        self.graph_combo.addItems([
            "Afρ от расстояния", 
            "Звездной величины от расстояния", 
            "Afρ от даты", 
            "Звездной величины от даты"
        ])

        combo_view = QListView()
        combo_view.setStyleSheet("""
            QListView {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #5f8bff;
            }
            QListView::item:selected {
                background-color: #aaccff;
                color: #000034;
            }
        """)        
        
        self.graph_combo.setView(combo_view)
        self.graph_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #5f8bff;
                border-radius: 10px;
                padding: 5px 25px 5px 10px;
                color: #000034;
                font-size: 14px;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #5f8bff;
                background-color: #aaccff;
            }
            QComboBox:on {
                border-bottom-left-radius: 0;
                border-bottom-right-radius: 0;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #5f8bff;
                border-top-right-radius: 9px;
                border-bottom-right-radius: 9px;
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
            }
        """)

        self.graph_combo.setEditable(False)
        self.graph_combo.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.graph_combo.view().window().setAttribute(Qt.WA_TranslucentBackground)

        graph_selector_layout.addWidget(graph_label)
        graph_selector_layout.addWidget(self.graph_combo)
        graph_selector_layout.addStretch()
        layout.addLayout(graph_selector_layout)
        layout.addSpacing(10)

    def init_graph_canvas(self, layout):
        graph_container = QFrame()
        graph_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: none;
            }
        """)
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(10, 10, 10, 10)
        
        self.figure = Figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#f8f8f8')
        
        graph_layout.addWidget(self.canvas)
        layout.addWidget(graph_container, 1)
        layout.addSpacing(15)

    def init_graph_controls(self, layout):
        controls = QHBoxLayout()
        controls.setAlignment(Qt.AlignCenter)
        
        button_data = [
            ("Приблизить", "zoom_in"),
            ("Отдалить", "zoom_out"),
            ("Сброс", "reset")
        ]
        
        for text, action in button_data:
            btn = QPushButton(text)
            btn.setFixedSize(150, 40)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: white;
                    border-radius: 20px;
                    border: none;
                    color: #000034;
                    font-size: 18px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #aaccff;
                }}
            """)
            btn.setCursor(Qt.PointingHandCursor)
            controls.addWidget(btn)
        
        controls.insertSpacing(1, 15)
        controls.insertSpacing(3, 15)
        
        layout.addLayout(controls)