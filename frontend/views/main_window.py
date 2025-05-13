from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt
from .help_window import HelpWindow
from .tabs.sublimation_tab import SublimationTab
from .tabs.graph_tab import GraphTab
from .tabs.mass_tab import MassTab
from .tabs.size_tab import SizeTab

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("КосмоМакарена3000")
        self.setFixedSize(900, 700)
        
        self.init_ui()
        self.init_tabs()
        self.show_tab("sublimation")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        import os
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'bg.jpeg').replace('\\', '/')
        self.setStyleSheet(f"""
            QMainWindow {{
                background-image: url("{image_path}");
                background-position: center;
                background-repeat: no-repeat;
                /* background-size: cover; */ /* Removed unsupported property */
                background-attachment: scroll;
            }}""")
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(70, 40, 70, 70)
        
        self.init_top_buttons(main_layout)
        self.init_content_area(main_layout)

    def init_top_buttons(self, layout):
        top_buttons = QHBoxLayout()
        top_buttons.setAlignment(Qt.AlignRight)

        self.load_btn = QPushButton("Загрузить данные")
        self.load_btn.setFixedSize(180, 40)
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 50, 0.6)rgba(11, 11, 200, 0.3);  
                border-radius: 20px;     
                border: 2px solid white;
                color: white;     
                font-size: 14px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(11, 11, 200, 0.3);  
            }
        """)
        self.load_btn.clicked.connect(self.load_data)
        top_buttons.addWidget(self.load_btn)

        self.help_btn = QPushButton("?")
        self.help_btn.setFixedSize(40, 40)
        self.help_btn.setStyleSheet("""
            QPushButton {
                background-color: white;  
                border-radius: 20px;    
                font-size: 24px;
                font-weight: bold;
                color: #000034;
                border: none;
                }
            QPushButton:hover {
                background-color: #aaccff;
                }
            """)
        self.help_btn.clicked.connect(self.show_help)
        top_buttons.addWidget(self.help_btn)
        
        layout.addLayout(top_buttons)

    def init_content_area(self, layout):
        content_frame = QFrame()
        content_frame.setFrameShape(QFrame.Box)
        content_frame.setLineWidth(2)
        content_frame.setStyleSheet("""
            background-color: #0b0b47;
            border-radius: 15px;
            border: 2px solid white;
        """)
        layout.addWidget(content_frame, 1)

        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 0, 20, 20)
        
        self.init_navigation_panel(content_layout)
        self.init_tabs_panel(content_layout)

    def init_navigation_panel(self, layout):
        left_panel = QFrame()
        left_panel.setFixedWidth(158)
        left_panel.setStyleSheet("""background-color: #0b0b47; border: none""")
        layout.addWidget(left_panel)
        layout.addSpacing(15)
        
        nav_layout = QVBoxLayout(left_panel)
        nav_layout.setSpacing(30)
        nav_layout.addSpacing(55)
        
        self.nav_buttons = []
        buttons = [
            ("Сублимация", "sublimation"),
            ("Графики", "graphs"),
            ("Масса комет", "mass"),
            ("Размеры ядра", "size")
        ]

        for text, tab_name in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(30)
            btn.setProperty('tab_name', tab_name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #000034;
                    border: none;
                    border-radius: 18px;
                    padding: 2px;
                    font-family: Arial;
                    font-size: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #aaccff;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedWidth(148)
            btn.setFixedHeight(50)
            btn.clicked.connect(lambda checked, tn=tab_name: self.show_tab(tn))
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        nav_layout.addStretch()

    def init_tabs_panel(self, layout):
        self.right_panel = QFrame()
        self.right_panel.setStyleSheet("""background-color: #0b0b47; border: none""")
        layout.addWidget(self.right_panel, 1)
        
        self.right_layout = QVBoxLayout(self.right_panel)

    def init_tabs(self):
        self.tabs = {
            "sublimation": SublimationTab(),
            "graphs": GraphTab(),
            "mass": MassTab(),
            "size": SizeTab()
        }
        
        for tab in self.tabs.values():
            self.right_layout.addWidget(tab)

    def show_tab(self, tab_name):
        for tab in self.tabs.values():
            tab.hide()
        
        self.tabs[tab_name].show()
        self.update_nav_buttons(tab_name)

    def update_nav_buttons(self, active_tab):
        for btn in self.nav_buttons:
            if btn.property('tab_name') == active_tab:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #5f8bff;
                        color: white;
                        border: none;
                        border-radius: 18px;
                        padding: 2px;
                        font-family: Arial;
                        font-size: 20px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #5f72eb;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        color: #000034;
                        border: none;
                        border-radius: 18px;
                        padding: 2px;
                        font-family: Arial;
                        font-size: 20px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #aaccff;
                    }
                """)

    def show_help(self):
        self.help_window = HelpWindow(self)
        self.help_window.show()
    
    def load_data(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Информация", "Функция загрузки данных будет реализована позже")