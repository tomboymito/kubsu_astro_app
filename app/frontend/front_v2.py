import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict.*")
import sys
from pathlib import Path
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, 
                             QScrollArea, QSizePolicy, QTextEdit, QListView)
from PyQt5.QtWidgets import QComboBox  
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QPainterPath
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import requests
import json

project_root = Path(__file__).parent.parent.parent  # Переходим на 3 уровня выше (из frontend)
sys.path.append(str(project_root))

# Импорт функций расчётов из backend
from app.backend.app.core.calculations.sublimation import calculate as calculate_sublimation_backend
from app.backend.app.core.calculations.mass import calculate as calculate_mass_backend
from app.backend.app.core.calculations.nucleus import calculate as calculate_nucleus_backend

# ======================================================================
# КОНСТАНТЫ И ВСПОМОГАТЕЛЬНЫЕ КЛАССЫ
# ======================================================================

class Meta(type(QMainWindow)):
    pass

class HelpWindow(QMainWindow, metaclass=Meta):
    """Окно справки с информацией о приложении и формулами"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справка")
        self.setFixedSize(900, 700)
        
        self.init_ui()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(60, 60, 60, 60)
        
        # Внешняя рамка
        outer_frame = self.create_outer_frame()
        layout.addWidget(outer_frame)
        
        # Внутренний layout
        inner_layout = QVBoxLayout(outer_frame)
        inner_layout.setContentsMargins(10, 10, 10, 10)
        
        # Область с прокруткой
        scroll_area = self.create_scroll_area()
        inner_layout.addWidget(scroll_area, 1)
        
        # Кнопка закрытия
        self.add_close_button(inner_layout)
    
    def create_outer_frame(self):
        """Создает внешнюю рамку окна"""
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(2)
        frame.setStyleSheet("""
            background-color: #0b0b47;
            border-radius: 20px;     
            border: 2px solid white;
        """)
        return frame
    
    def create_scroll_area(self):
        """Создает область с прокруткой и контентом"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(self.get_scroll_area_style())
        
        # Виджет контента
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #0b0b47; border: none;")
        
        # Layout контента
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Добавление текста справки
        content = self.create_help_content()
        content_layout.addWidget(content)
        
        scroll_area.setWidget(content_widget)
        return scroll_area
    
    def get_scroll_area_style(self):
        """Возвращает стили для области прокрутки"""
        return """
            QScrollArea {
                border: none;
                background-color: #0b0b47;
            }
            QScrollBar:vertical {
                border: none;
                background: #0b0b47;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """
    
    def create_help_content(self):
        """Создает содержимое справки"""
        content = QLabel(self.get_help_text())
        content.setStyleSheet("""
            background-color: #0b0b47;
            border-radius: 20px;      
            color: white;
            border: none;
            padding: 20px;
        """)
        content.setWordWrap(True)
        content.setAlignment(Qt.AlignJustify)
        return content
    
    def get_help_text(self):
        """Возвращает текст справки в HTML формате"""
        return """
        <div style='font-family: Arial; color: white; text-align: justify;'>
            <div style='font-family: Arial; color: white; text-align: justify;'>
                <!-- Содержимое справки -->
                <h3 style='text-align: left;'>Памятка по использованию приложения</h3>
                <p><b>Общее руководство.</b></p>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    - Приложение разработано для выполнения заданий Астрохакатона 2025, включая расчет сублимации, построение графиков, определение массы комет и размеров их ядер.<br>
                    - Интерфейс состоит из четырех вкладок: "Сублимация", "Графики", "Масса" и "Размеры ядра".
                </div>

                <!-- Остальной текст справки ... -->
            </div>
        </div>
        """
    
    def add_close_button(self, layout):
        """Добавляет кнопку закрытия в layout"""
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
        layout.addWidget(self.close_btn, 0, Qt.AlignBottom | Qt.AlignHCenter)

# ======================================================================
# ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ
# ======================================================================

class MainApplication(QMainWindow):
    """Главное окно приложения"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("КосмоМакарена3000")
        self.setFixedSize(900, 700)
        
        self.init_ui()
        self.init_tabs()
    
    def init_ui(self):
        """Инициализация основного интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Remove stylesheet background image due to pixmap and unsupported property issues
        # Instead, background will be painted in paintEvent

        # Основной layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(70, 40, 70, 70)
        
        # Добавление верхних кнопок
        self.add_top_buttons(main_layout)
        
        # Основная область контента
        self.add_content_area(main_layout)
    
    def paintEvent(self, event):
        """Переопределение paintEvent для рисования фонового изображения с масштабированием"""
        from PyQt5.QtGui import QPainter, QPixmap
        import os

        painter = QPainter(self)
        # Construct absolute path to bg.jpeg
        bg_path = os.path.join(os.path.dirname(__file__), "bg.jpeg")
        pixmap = QPixmap(bg_path)
        if pixmap.isNull():
            print(f"Error: Could not load pixmap from {bg_path}")
        else:
            # Scale pixmap to window size
            scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            # Draw pixmap starting at top-left corner
            painter.drawPixmap(0, 0, scaled_pixmap)
    
    def add_top_buttons(self, layout):
        """Добавляет кнопки в верхнюю часть окна"""
        top_buttons = QHBoxLayout()
        top_buttons.setAlignment(Qt.AlignRight)

        # Кнопка загрузки данных
        self.load_btn = self.create_button("Загрузить данные", 180, 40, """
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

        # Кнопка справки
        self.help_btn = self.create_button("?", 40, 40, """
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
    
    def create_button(self, text, width, height, style):
        """Создает кнопку с заданными параметрами"""
        btn = QPushButton(text)
        btn.setFixedSize(width, height)
        btn.setStyleSheet(style)
        btn.setCursor(Qt.PointingHandCursor)
        return btn
    
    def add_content_area(self, layout):
        """Добавляет основную область контента"""
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
        
        # Левая панель с навигацией
        self.add_navigation_panel(content_layout)
        
        # Правая панель с вкладками
        self.add_tabs_panel(content_layout)
    
    def add_navigation_panel(self, layout):
        """Добавляет панель навигации"""
        left_panel = QFrame()
        left_panel.setFixedWidth(158)
        left_panel.setStyleSheet("""
            background-color: #0b0b47;
            border: none
        """)
        layout.addWidget(left_panel)
        layout.addSpacing(15)
        
        nav_layout = QVBoxLayout(left_panel)
        nav_layout.setSpacing(30)
        nav_layout.addSpacing(55)
        
        # Создание кнопок навигации
        self.nav_buttons = []
        buttons = [
            ("Сублимация", "sublimation"),
            ("Графики", "graphs"),
            ("Масса", "mass"),
            ("Размеры ядра", "size")
        ]

        for text, tab_name in buttons:
            btn = self.create_nav_button(text, tab_name)
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        nav_layout.addStretch()

    def create_input_frame(self, fields):
        """Создает фрейм с полями ввода"""
        frame = QWidget()
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        
        # Заголовок
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
        layout.addLayout(row1)
        
        # Поля ввода
        for i, (label_text, width) in enumerate(fields, start=2):
            row = QHBoxLayout()
            row.setSpacing(10)
            
            param_label = QLabel(label_text)
            param_label.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 14px;
                    color: white;
                    border: 2px solid #aaaaaa;
                    border-radius: 7px;
                    padding: 5px;
                }
            """)
            param_label.setFixedWidth(width)
            row.addWidget(param_label)
            
            input_field = QLineEdit()
            input_field.setMaximumHeight(40)
            input_field.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #aaaaaa;
                    border-radius: 7px;
                    padding: 5px;
                    color: white;
                }
            """)
            row.addWidget(input_field, 1)
            
            # Сохраняем ссылки на поля ввода
            setattr(self, f"input{i-1}", input_field)
            
            layout.addLayout(row)
        
        return frame

    def create_output_group(self):
        """Создает группу для вывода результата"""
        group = QWidget()
        layout = QVBoxLayout(group)
        layout.setContentsMargins(0, 0, 0, 0)
        
        output_label = QLabel("Результат")
        output_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
                color: white;
                border: none;
                padding: 5px;
            }
        """)
        output_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a4d;
                border-radius: 10px;
                color: white;
                font-size: 14px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.output_text)
        
        return group
    
    def create_nav_button(self, text, tab_name):
        """Создает кнопку навигации"""
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
        return btn
    
    def add_tabs_panel(self, layout):
        """Добавляет панель с вкладками"""
        self.right_panel = QFrame()
        self.right_panel.setStyleSheet("""
            background-color: #0b0b47;
            border: none
        """)
        layout.addWidget(self.right_panel, 1)
        
        self.right_layout = QVBoxLayout(self.right_panel)
    
    def init_tabs(self):
        """Инициализирует вкладки приложения"""
        self.tabs = {
            "sublimation": self.create_sublimation_tab("Сублимация"),
            "graphs": QWidget(),  # Заглушка для вкладки графиков, т.к. create_graph_tab отсутствует
            "mass": self.create_mass_tab("Масса комет"),
            "size": self.create_size_tab("Размеры ядра")
        }
        
        for tab in self.tabs.values():
            self.right_layout.addWidget(tab)
        
        # Показываем начальную вкладку
        self.show_tab("sublimation")

    def create_sublimation_tab(self, title):
        """Создает вкладку для расчета сублимации"""
        tab = QWidget()
        tab.setStyleSheet("""
            background-color: #0b0b47;
            border: none
        """)
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Поля ввода
        input_frame = self.create_input_frame([
            ("Температура (К):", 205),
            ("Расстояние от Земли (а.е):", 205),
            ("Расстояние от солнца (а.е):", 205)
        ])
        layout.addWidget(input_frame)
        
        # Кнопка расчета
        self.calc_btn_sublimation = self.create_button("Рассчитать", 519, 40, """
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
        self.calc_btn_sublimation.clicked.connect(self.calculate_sublimation)
        layout.addWidget(self.calc_btn_sublimation)
        layout.addSpacing(10)

        # Поле вывода
        output_group = self.create_output_group()
        layout.addWidget(output_group, 1)

        return tab

    def create_mass_tab(self, title):
        """Создает вкладку для расчета массы"""
        tab = QWidget()
        tab.setStyleSheet("""
            background-color: #0b0b47;
            border: none
        """)
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Поля ввода
        input_frame = self.create_input_frame([
            ("Видимая звездная величина (m<sub>k</sub>):", 255),
            ("Расстояние (Δ):", 255),
            ("Радиус (r):", 255)
        ])
        layout.addWidget(input_frame)
        
        # Кнопка расчета
        self.calc_btn_mass = self.create_button("Рассчитать", 519, 40, """
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
        self.calc_btn_mass.clicked.connect(self.calculate_mass)
        layout.addWidget(self.calc_btn_mass)
        layout.addSpacing(10)

        # Поле вывода
        output_group = self.create_output_group()
        layout.addWidget(output_group, 1)

        return tab

    def create_size_tab(self, title):
        """Создает вкладку для расчета размеров ядра"""
        tab = QWidget()
        tab.setStyleSheet("""
            background-color: #0b0b47;
            border: none
        """)
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Поля ввода
        input_frame = self.create_input_frame([
            ("Абсолютная звездная величина (H):", 270),
            ("Альбедо (p):", 270),
            ("Угловой размер:", 270)
        ])
        layout.addWidget(input_frame)
        
        # Кнопка расчета
        self.calc_btn_size = self.create_button("Рассчитать", 519, 40, """
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
        self.calc_btn_size.clicked.connect(self.calculate_size)
        layout.addWidget(self.calc_btn_size)
        layout.addSpacing(10)

        # Поле вывода
        output_group = self.create_output_group()
        layout.addWidget(output_group, 1)

        return tab

# ======================================================================
# МЕТОДЫ ДЛЯ РАБОТЫ С ВКЛАДКАМИ И ДАННЫМИ
# ======================================================================

    def show_tab(self, tab_name):
        """Показывает указанную вкладку"""
        # Скрываем все вкладки
        for tab in self.tabs.values():
            tab.hide()
        
        # Показываем нужную вкладку
        self.tabs[tab_name].show()
        
        # Обновляем стили кнопок навигации
        self.update_nav_buttons(tab_name)

    def update_nav_buttons(self, active_tab):
        """Обновляет стили кнопок навигации"""
        for btn in self.nav_buttons:
            if btn.property('tab_name') == active_tab:
                # Стиль для активной кнопки
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
        """Показывает окно справки"""
        self.help_window = HelpWindow(self)
        self.help_window.show()
    
    def load_data(self):
        """Загружает данные из файла"""
        QMessageBox.information(self, "Информация", "Функция загрузки данных будет реализована позже")
    
    def api_calculate(self, calculation_type, parameters):
        """Вспомогательный метод для вызова backend API расчета"""
        url = "http://localhost:8000/api/calculate"
        try:
            response = requests.post(
                url,
                data={
                    "calculation_type": calculation_type,
                    "parameters": json.dumps(parameters)
                }
            )
            response.raise_for_status()
            data = response.json()
            if data.get("error"):
                raise Exception(data["error"])
            return data.get("result"), data.get("units")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при вызове API: {str(e)}")
            return None, None

    def calculate_sublimation(self):
        """Выполняет расчет сублимации"""
        try:
            temperature = float(self.input1.text())
            earth_distance = float(self.input2.text())
            sun_distance = float(self.input3.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, введите корректные числовые значения.")
            return
        
        params = {
            "temperature": temperature,
            "earth_distance": earth_distance,
            "sun_distance": sun_distance
        }
        result, units = self.api_calculate("sublimation", params)
        if result is not None:
            self.output_text.setPlainText(f"Результат: {result} {units}")
    
    def calculate_mass(self):
        """Выполняет расчет массы"""
        try:
            m_k = float(self.input1.text())
            delta = float(self.input2.text())
            radius = float(self.input3.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, введите корректные числовые значения.")
            return
        
        params = {
            "m_k": m_k,
            "delta": delta,
            "radius": radius
        }
        result, units = self.api_calculate("mass", params)
        if result is not None:
            self.output_text.setPlainText(f"Результат: {result} {units}")
    
    def calculate_size(self):
        """Выполняет расчет размеров"""
        try:
            H = float(self.input1.text())
            p = float(self.input2.text())
            angular_size = float(self.input3.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, введите корректные числовые значения.")
            return
        
        params = {
            "H": H,
            "p": p,
            "angular_size": angular_size
        }
        result, units = self.api_calculate("nucleus", params)
        if result is not None:
            self.output_text.setPlainText(f"Результат: {result} {units}")

# ======================================================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# ======================================================================

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    app = QApplication(sys.argv)
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())