import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, 
                             QScrollArea, QSizePolicy, QTextEdit, QListView)
from PyQt5.QtWidgets import QComboBox  
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QPainterPath
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class HelpWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справка")
        self.setFixedSize(900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(60, 60, 60, 60)
        
        # Outer frame
        outer_frame = QFrame()
        outer_frame.setFrameShape(QFrame.Box)
        outer_frame.setLineWidth(2)
        outer_frame.setStyleSheet("""background-color: #0b0b47;
        border-radius: 20px;     
        border: 2px solid white;
        """)
        layout.addWidget(outer_frame)
        
        # Inner layout
        inner_layout = QVBoxLayout(outer_frame)
        inner_layout.setContentsMargins(10, 10, 10, 10)
        
        # Content
        content = QLabel("""Здесь будет справочная информация""")
        content.setStyleSheet("""background-color: #0b0b47;
        border-radius: 20px;      
        color: white;
        border: none;
        """)
        content.setAlignment(Qt.AlignCenter)
        inner_layout.addWidget(content, 1)
        
        # Close button

        self.close_btn = QPushButton("Спасибо!")
        self.close_btn.setFixedSize(750, 40)  # Квадратная кнопка
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

        self.close_btn.clicked.connect(self.close)
        inner_layout.addWidget(self.close_btn, 0, Qt.AlignBottom | Qt.AlignHCenter)

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("КосмоМакарена3000")
        self.setFixedSize(900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)


        self.setStyleSheet("""
            QMainWindow {
                background-image: url("bg.jpeg");
                background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
        background-attachment: scroll;
            }""")
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(70, 40, 70, 70)
        
        # Top buttons frame
        top_buttons = QHBoxLayout()
        top_buttons.setAlignment(Qt.AlignRight)

        self.load_btn = QPushButton("Загрузить данные")
        self.load_btn.setFixedSize(180, 40)  # Квадратная кнопка
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
        self.help_btn.setFixedSize(40, 40)  # Квадратная кнопка
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

        
        main_layout.addLayout(top_buttons)

        # Main content area
        content_frame = QFrame()
        content_frame.setFrameShape(QFrame.Box)
        content_frame.setLineWidth(2)
        content_frame.setStyleSheet("""
    background-color: #0b0b47;
    border-radius: 15px;
    border: 2px solid white;
""")
        main_layout.addWidget(content_frame, 1)

        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 0, 20, 20)
        
        # Left panel (navigation)
        left_panel = QFrame()
        left_panel.setFixedWidth(158)
        left_panel.setStyleSheet("""background-color: #0b0b47;
        border: none""")
        content_layout.addWidget(left_panel)
        content_layout.addSpacing(15)
        
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
            btn.setProperty('tab_name', tab_name)  # Добавляем свойство с именем вкладки
            
            # Стандартный стиль
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
            self.nav_buttons.append(btn)  # Добавляем кнопку в список
            
            
        nav_layout.addStretch()
        
        # Right panel (tabs)
        self.right_panel = QFrame()
        self.right_panel.setStyleSheet("""background-color: #0b0b47;
        border: none
        """)
        content_layout.addWidget(self.right_panel, 1)
        
        # Create tabs
        self.tabs = {
            "sublimation": self.create_sublimation_tab("Сублимация"),
            "graphs": self.create_graph_tab(),
            "mass": self.create_mass_tab("Масса комет"),
            "size": self.create_size_tab("Размеры ядра")
        }
        
        # Stack all tabs in right panel
        self.right_layout = QVBoxLayout(self.right_panel)
        for tab in self.tabs.values():
            self.right_layout.addWidget(tab)
        
        # Show initial tab
        self.show_tab("sublimation")

        #create_data_tab

    def create_sublimation_tab(self, title):
        tab = QWidget()
        tab.setStyleSheet("""background-color: #0b0b47;
        border: none
        """)
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Input fields
        input_frame = QWidget()
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(10)

        param_label_style = """
        QLabel {
            font-weight: bold;
            font-size: 14px;
            color: white;
            border: 2px solid #aaaaaa;
            border-radius: 7px;
            padding: 5px;
        }
        """
        
        row1 = QHBoxLayout()
        row1.setSpacing(5)
        param_label1 = QLabel("Параметры для рассчета")
        param_label1.setStyleSheet("""
        QLabel {
            font-weight: bold;
            font-size: 16px;
            color: white;
            border: none;
            padding: 5px;
        }
        """)

        
        param_label1.setFixedWidth(504)
        param_label1.setFixedHeight(40)
        param_label1.setAlignment(Qt.AlignCenter)
        row1.addWidget(param_label1)
        input_layout.addLayout(row1)

        # Первое поле ввода
        row2 = QHBoxLayout()
        row2.setSpacing(10)
        param_label1 = QLabel("Температура (К):")
        param_label1.setStyleSheet(param_label_style)
        param_label1.setFixedWidth(205)
        row2.addWidget(param_label1)
        self.input1 = QLineEdit()
        self.input1.setMaximumHeight(40)
        self.input1.setStyleSheet("""
            QLineEdit {
                border: 2px solid #aaaaaa;
                border-radius: 7px;
                padding: 5px;
                color: white;
            }
        """)
        row2.addWidget(self.input1, 1)
        input_layout.addLayout(row2)
        
        # Второе поле ввода
        row3 = QHBoxLayout()
        row3.setSpacing(10)
        param_label2 = QLabel("Расстояние от Земли (а.е):")
        param_label2.setStyleSheet(param_label_style)
        param_label2.setFixedWidth(205)
        row3.addWidget(param_label2)
        self.input2 = QLineEdit()
        self.input2.setMaximumHeight(40)
        self.input2.setStyleSheet("""
            QLineEdit {
                border: 2px solid #aaaaaa;
                border-radius: 7px;
                padding: 5px;
                color: white;
            }
        """)
        row3.addWidget(self.input2, 1)
        input_layout.addLayout(row3)
        
        # Третье поле ввода
        row4 = QHBoxLayout()
        row4.setSpacing(10)
        param_label3 = QLabel("Расстояние от солнца (а.е):")
        param_label3.setStyleSheet(param_label_style)
        param_label3.setFixedWidth(205)
        row4.addWidget(param_label3)
        self.input3 = QLineEdit()
        self.input3.setMaximumHeight(40)
        self.input3.setStyleSheet("""
            QLineEdit {
                border: 2px solid #aaaaaa;
                border-radius: 7px;
                padding: 5px;
                color: white;
            }
        """)
        row4.addWidget(self.input3, 1)
        input_layout.addLayout(row4)
        
        layout.addWidget(input_frame)


        
        # Calculate button
        
        self.calc_btn = QPushButton("Рассчитать")
        self.calc_btn.setCursor(Qt.PointingHandCursor)
        self.calc_btn.setFixedSize(519, 40)  # Фиксированный размер
        self.calc_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 20px;
                border: none;
                color: #000034;
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #aaccff;
                
            }
            """)
        self.calc_btn.clicked.connect(self.calculate_sublimation)  # Предполагая, что есть метод calculate
        layout.addWidget(self.calc_btn)
        layout.addSpacing(10)

        # Output area
        output_group = QFrame()
        output_group.setStyleSheet("""
        QFrame {
            border: 2px solid #aaaaaa;
            border-radius: 8px;
            padding: 5px;
        }
        """)
        output_layout = QVBoxLayout(output_group)
        output_layout.setContentsMargins(5, 5, 5, 5)

        output_label = QLabel("Результаты вычислений:")
        output_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white; border: none;")
        output_layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("""
        QTextEdit {
        background-color: white;
            border: 1px solid #aaaaaa;
            border-radius: 5px;
            padding: 5px;
            font-family: Consolas;
            color: #000034;
        }
        """)

        output_layout.addWidget(self.output_text)
        layout.addWidget(output_group, 1)

        return tab

    def create_mass_tab(self, title):
            tab = QWidget()
            tab.setStyleSheet("""background-color: #0b0b47;
            border: none
            """)
            layout = QVBoxLayout(tab)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # Input fields
            input_frame = QWidget()
            input_layout = QVBoxLayout(input_frame)
            input_layout.setSpacing(10)

            param_label_style = """
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: white;
                border: 2px solid #aaaaaa;
                border-radius: 7px;
                padding: 5px;
            }
            """
            
            row1 = QHBoxLayout()
            row1.setSpacing(5)
            param_label1 = QLabel("Параметры для рассчета")
            param_label1.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
                color: white;
                border: none;
                padding: 5px;
            }
            """)

            param_label1.setFixedWidth(504)
            param_label1.setFixedHeight(40)
            param_label1.setAlignment(Qt.AlignCenter)
            row1.addWidget(param_label1)
            input_layout.addLayout(row1)

            # Первое поле ввода
            row2 = QHBoxLayout()
            row2.setSpacing(10)
            param_label1 = QLabel("Видимая звездная величина (m<sub>k</sub>):")
            param_label1.setStyleSheet(param_label_style)
            param_label1.setFixedWidth(255)
            row2.addWidget(param_label1)
            self.input1 = QLineEdit()
            self.input1.setMaximumHeight(40)
            self.input1.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #aaaaaa;
                    border-radius: 7px;
                    padding: 5px;
                    color: white;
                }
            """)
            row2.addWidget(self.input1, 1)
            input_layout.addLayout(row2)
            
            # Второе поле ввода
            row3 = QHBoxLayout()
            row3.setSpacing(10)
            param_label2 = QLabel("Расстояние (Δ):")
            param_label2.setStyleSheet(param_label_style)
            param_label2.setFixedWidth(255)
            row3.addWidget(param_label2)
            self.input2 = QLineEdit()
            self.input2.setMaximumHeight(40)
            self.input2.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #aaaaaa;
                    border-radius: 7px;
                    padding: 5px;
                    color: white;
                }
            """)
            row3.addWidget(self.input2, 1)
            input_layout.addLayout(row3)
            
            # Третье поле ввода
            row4 = QHBoxLayout()
            row4.setSpacing(10)
            param_label3 = QLabel("Радиус (r):")
            param_label3.setStyleSheet(param_label_style)
            param_label3.setFixedWidth(255)
            row4.addWidget(param_label3)
            self.input3 = QLineEdit()
            self.input3.setMaximumHeight(40)
            self.input3.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #aaaaaa;
                    border-radius: 7px;
                    padding: 5px;
                    color: white;
                }
            """)
            row4.addWidget(self.input3, 1)
            input_layout.addLayout(row4)
            
            layout.addWidget(input_frame)


            
            # Calculate button
        
            self.calc_btn = QPushButton("Рассчитать")
            self.calc_btn.setCursor(Qt.PointingHandCursor)
            self.calc_btn.setFixedSize(519, 40)  # Фиксированный размер
            self.calc_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 20px;
                border: none;
                color: #000034;
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #aaccff;
                
            }
            """)
            self.calc_btn.clicked.connect(self.calculate_sublimation)  # Предполагая, что есть метод calculate
            layout.addWidget(self.calc_btn)
            layout.addSpacing(10)

            # Output area
            output_group = QFrame()
            output_group.setStyleSheet("""
            QFrame {
                border: 2px solid #aaaaaa;
                border-radius: 8px;
                padding: 5px;
            }
            """)
            output_layout = QVBoxLayout(output_group)
            output_layout.setContentsMargins(5, 5, 5, 5)

            output_label = QLabel("Результаты вычислений:")
            output_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white; border: none;")
            output_layout.addWidget(output_label)

            self.output_text = QTextEdit()
            self.output_text.setReadOnly(True)
            self.output_text.setStyleSheet("""
            QTextEdit {
            background-color: white;
                border: 1px solid #aaaaaa;
                border-radius: 5px;
                padding: 5px;
                font-family: Consolas;
                color: #000034;
            }
            """)

            output_layout.addWidget(self.output_text)
            layout.addWidget(output_group, 1)

            return tab

    def create_size_tab(self, title):
            tab = QWidget()
            tab.setStyleSheet("""background-color: #0b0b47;
            border: none
            """)
            layout = QVBoxLayout(tab)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # Input fields
            input_frame = QWidget()
            input_layout = QVBoxLayout(input_frame)
            input_layout.setSpacing(10)

            param_label_style = """
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: white;
                border: 2px solid #aaaaaa;
                border-radius: 7px;
                padding: 5px;
            }
            """
            
            row1 = QHBoxLayout()
            row1.setSpacing(5)
            param_label1 = QLabel("Параметры для рассчета")
            param_label1.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
                color: white;
                border: none;
                padding: 5px;
            }
            """)

            
            param_label1.setFixedWidth(504)
            param_label1.setFixedHeight(40)
            param_label1.setAlignment(Qt.AlignCenter)
            row1.addWidget(param_label1)
            input_layout.addLayout(row1)

            # Первое поле ввода
            row2 = QHBoxLayout()
            row2.setSpacing(10)
            param_label1 = QLabel("Абсолютная звездная величина (H):")
            param_label1.setStyleSheet(param_label_style)
            param_label1.setFixedWidth(270)
            row2.addWidget(param_label1)
            self.input1 = QLineEdit()
            self.input1.setMaximumHeight(40)
            self.input1.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #aaaaaa;
                    border-radius: 7px;
                    padding: 5px;
                    color: white;
                }
            """)
            row2.addWidget(self.input1, 1)
            input_layout.addLayout(row2)
            
            # Второе поле ввода
            row3 = QHBoxLayout()
            row3.setSpacing(10)
            param_label2 = QLabel("Альбедо (p):")
            param_label2.setStyleSheet(param_label_style)
            param_label2.setFixedWidth(270)
            row3.addWidget(param_label2)
            self.input2 = QLineEdit()
            self.input2.setMaximumHeight(40)
            self.input2.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #aaaaaa;
                    border-radius: 7px;
                    padding: 5px;
                    color: white;
                }
            """)
            row3.addWidget(self.input2, 1)
            input_layout.addLayout(row3)
            
            # Третье поле ввода
            row4 = QHBoxLayout()
            row4.setSpacing(10)
            param_label3 = QLabel("Угловой размер:")
            param_label3.setStyleSheet(param_label_style)
            param_label3.setFixedWidth(270)
            row4.addWidget(param_label3)
            self.input3 = QLineEdit()
            self.input3.setMaximumHeight(40)
            self.input3.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #aaaaaa;
                    border-radius: 7px;
                    padding: 5px;
                    color: white;
                }
            """)
            row4.addWidget(self.input3, 1)
            input_layout.addLayout(row4)
            
            layout.addWidget(input_frame)

            # Calculate button
            self.calc_btn = QPushButton("Рассчитать")
            self.calc_btn.setCursor(Qt.PointingHandCursor)
            self.calc_btn.setFixedSize(519, 40)  # Фиксированный размер
            self.calc_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 20px;
                border: none;
                color: #000034;
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #aaccff;
                
            }
            """)
            self.calc_btn.clicked.connect(self.calculate_sublimation)  # Предполагая, что есть метод calculate
            layout.addWidget(self.calc_btn)
            layout.addSpacing(10)

            # Output area
            output_group = QFrame()
            output_group.setStyleSheet("""
            QFrame {
                border: 2px solid #aaaaaa;
                border-radius: 8px;
                padding: 5px;
            }
            """)
            output_layout = QVBoxLayout(output_group)
            output_layout.setContentsMargins(5, 5, 5, 5)

            output_label = QLabel("Результаты вычислений:")
            output_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white; border: none;")
            output_layout.addWidget(output_label)

            self.output_text = QTextEdit()
            self.output_text.setReadOnly(True)
            self.output_text.setStyleSheet("""
            QTextEdit {
            background-color: white;
                border: 1px solid #aaaaaa;
                border-radius: 5px;
                padding: 5px;
                font-family: Consolas;
                color: #000034;
            }
            """)

            output_layout.addWidget(self.output_text)
            layout.addWidget(output_group, 1)

            return tab

    def create_graph_tab(self):
        tab = QWidget()
        tab.setStyleSheet("background-color: #0b0b47;")
        layout = QVBoxLayout(tab)
        
        # Выпадающее меню для выбора графиков
        graph_selector_layout = QHBoxLayout()
        graph_label = QLabel("Тип графика:")
        graph_label.setStyleSheet("""
            color: white; 
            font-weight: bold; 
            font-size: 16px;
        """)

        # Создаем выпадающий список
        self.graph_combo = QComboBox()
        self.graph_combo.addItems(["Afρ от расстояния", "Звездной величины от расстояния", "Afρ от даты", "Звездной величины от даты"])


        # 2. Настройка view для скругленных углов
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

        # 3. Основной стиль комбобокса только закрытой его части
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

        # Дополнительные настройки
        self.graph_combo.setEditable(False)  # Запрещаем редактирование
        self.graph_combo.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint
        )  # Убираем стандартные рамки
        self.graph_combo.view().window().setAttribute(
            Qt.WA_TranslucentBackground
        )  # Прозрачный фон окна

        graph_selector_layout.addWidget(graph_label)
        graph_selector_layout.addWidget(self.graph_combo)
        graph_selector_layout.addStretch()
        layout.addLayout(graph_selector_layout)

        layout.addSpacing(10)
        
        # Контейнер для графика с скруглёнными углами
        graph_container = QFrame()
        graph_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: none;
            }
        """)
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(10, 10, 10, 10)  # Внутренние отступы
        
        # Matplotlib canvas
        self.figure = Figure(facecolor='white')  # Прозрачный фон фигуры
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#f8f8f8')  # Светло-серый фон области графика
        
        graph_layout.addWidget(self.canvas)
        layout.addWidget(graph_container, 1)
        layout.addSpacing(15)
        
        # Graph controls with circular buttons
        controls = QHBoxLayout()
        controls.setAlignment(Qt.AlignCenter)
        
        button_data = [
            ("Приблизить", "zoom_in"),
            ("Отдалить", "zoom_out"),
            ("Сброс", "reset")
        ]
        
        for text, action in button_data:
            btn = QPushButton(text)
            btn.setFixedSize(150, 40)  # Квадратная кнопка для круга
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
        
        # Добавляем отступы между кнопками
        controls.insertSpacing(1, 15)  # После первой кнопки
        controls.insertSpacing(3, 15)  # После второй кнопки
        
        layout.addLayout(controls)
        
        return tab
    
    def show_tab(self, tab_name):
    # Скрываем все вкладки
        for tab in self.tabs.values():
            tab.hide()
        
        # Показываем нужную вкладку
        self.tabs[tab_name].show()
        
        # Обновляем стили кнопок навигации
        self.update_nav_buttons(tab_name)

    def update_nav_buttons(self, active_tab):
        for btn in self.nav_buttons:
            if btn.property('tab_name') == active_tab:
                # Стиль для активной кнопки
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #5f8bff;  /* Красный цвет */
                        color: white;
                        border: none;
                        border-radius: 18px;
                        padding: 2px;
                        font-family: Arial;
                        font-size: 20px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #5f72eb;  /* Светлее при наведении */
                    }
                """)
            else:
                # Стандартный стиль
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
        QMessageBox.information(self, "Информация", "Функция загрузки данных будет реализована позже")
    
    import requests
    import json

    def calculate_sublimation(self):
        try:
            params = {
                "temperature": float(self.input1.text()),
                "distance_earth": float(self.input2.text()),
                "distance_sun": float(self.input3.text())
            }
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные числовые значения.")
            return

        data = {
            "calculation_type": "sublimation",
            "parameters": params
        }
        try:
            response = requests.post("http://localhost:8000/api/calculate", data={
                "calculation_type": "sublimation",
                "parameters": json.dumps(params)
            })
            response.raise_for_status()
            result = response.json()
            if result.get("error"):
                QMessageBox.warning(self, "Ошибка", f"Ошибка расчета: {result['error']}")
            else:
                self.output_text.setText(f"Результат: {result.get('result')} {result.get('units')}")
        except requests.RequestException as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка соединения с сервером: {str(e)}")

    def calculate_mass(self):
        try:
            params = {
                "magnitude": float(self.input1.text()),
                "distance": float(self.input2.text()),
                "radius": float(self.input3.text())
            }
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные числовые значения.")
            return

        try:
            response = requests.post("http://localhost:8000/api/calculate", data={
                "calculation_type": "mass",
                "parameters": json.dumps(params)
            })
            response.raise_for_status()
            result = response.json()
            if result.get("error"):
                QMessageBox.warning(self, "Ошибка", f"Ошибка расчета: {result['error']}")
            else:
                self.output_text.setText(f"Результат: {result.get('result')} {result.get('units')}")
        except requests.RequestException as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка соединения с сервером: {str(e)}")

    def calculate_size(self):
        try:
            params = {
                "absolute_magnitude": float(self.input1.text()),
                "albedo": float(self.input2.text()),
                "angular_size": float(self.input3.text())
            }
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные числовые значения.")
            return

        try:
            response = requests.post("http://localhost:8000/api/calculate", data={
                "calculation_type": "nucleus",
                "parameters": json.dumps(params)
            })
            response.raise_for_status()
            result = response.json()
            if result.get("error"):
                QMessageBox.warning(self, "Ошибка", f"Ошибка расчета: {result['error']}")
            else:
                self.output_text.setText(f"Результат: {result.get('result')} {result.get('units')}")
        except requests.RequestException as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка соединения с сервером: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())