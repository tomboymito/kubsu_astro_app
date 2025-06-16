import os
import sys
import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFrame,
    QMessageBox,
    QScrollArea,
    QTextEdit,
    QListView,
    QFileDialog,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib as mpl

def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу, работает для dev и для PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class CustomNavigationToolbar(NavigationToolbar):
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Home', 'Back', 'Forward', 'Pan', 'Zoom', 'Save')]
    
    def __init__(self, canvas, parent=None):
        super().__init__(canvas, parent)
        self._update_icons()

        self.setStyleSheet("color: white;")

        for attr in ("_coordinates", "coordinates", "coordinates_label"):
            widget = getattr(self, attr, None)
            if widget is not None and hasattr(widget, "setStyleSheet"):
                widget.setStyleSheet("color: white;")

        for label in self.findChildren(QLabel):
            if hasattr(label, "setStyleSheet"):
                label.setStyleSheet("color: white;")
    
    def _update_icons(self):
        icon_mapping = {
            'Home': 'home.png',
            'Back': 'back.png',
            'Forward': 'forward.png',
            'Pan': 'pan.png',
            'Zoom': 'zoom.png',
            'Save': 'save.png'
        }

        icons_dir = os.path.join(os.path.dirname(__file__), '..', 'icons')
        
        if not os.path.exists(icons_dir):
            print(f"Папка с иконками не найдена: {icons_dir}")
            return

        for action in self.actions():
            action_text = action.text() if action.text() else ""
            
            for action_name, icon_file in icon_mapping.items():
                if action_name in action_text:
                    icon_path = os.path.join(icons_dir, icon_file)
                    if os.path.exists(icon_path):
                        action.setIcon(QIcon(icon_path))
                    else:
                        print(f"Файл иконки не найден: {icon_path}")
                    break

class HelpWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справка")
        self.setFixedSize(1100, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        background = QLabel(central_widget)
        background.setScaledContents(True)
        pixmap = QPixmap(resource_path("data/bg.jpeg"))
        if not pixmap.isNull():
            background.setPixmap(pixmap)
        else:
            background.setStyleSheet("background-color: #0b0b47;")
        background.setGeometry(0, 0, self.width(), self.height())
        background.lower()
        
        content_container = QWidget()
        content_container.setStyleSheet("background: transparent;")
        main_layout.addWidget(content_container)
        
        layout = QVBoxLayout(content_container)
        layout.setContentsMargins(60, 60, 60, 60)
        
        outer_frame = QFrame()
        outer_frame.setFrameShape(QFrame.Box)
        outer_frame.setLineWidth(2)
        outer_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(11, 11, 71, 0.85);
                border-radius: 20px;
                border: 2px solid white;
            }
        """)
        layout.addWidget(outer_frame)
        
        inner_layout = QVBoxLayout(outer_frame)
        inner_layout.setContentsMargins(10, 10, 10, 10)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: white;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, 
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        content = QLabel("""
        <div style='font-family: Arial; color: white; text-align: justify;'>
            <div style='font-family: Arial; color: white; text-align: justify;'>

                <h3 style='text-align: left;'>Памятка по использованию приложения</h3>

                <p><b>Общее руководство.</b></p>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    - Приложение разработано для выполнения заданий Астрохакатона 2025, включая расчет сублимации, построение графиков, определение массы комет и размеров их ядер.<br>
                    - Интерфейс состоит из четырех вкладок: "Сублимация", "Графики", "Масса" и "Размеры ядра".
                </div>

                <br><br>
                <h3 style='text-align: left;'>Пошаговое использование.</h3>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    <b>- Запуск:</b> Откройте приложение, выберите нужную вкладку.<br>
                    <b>- Загрузка данных:</b> Нажмите "Загрузить файл" и выберите .txt файл с параметрами.<br>
                    <b>- Ввод данных:</b> Введите параметры вручную в соответствующие поля с валидацией.<br>
                    <b>Расчет:</b> Нажмите "Рассчитать" для получения результатов.<br>
                    <b>Визуализация:</b> Просмотрите таблицы, графики или текстовые результаты.<br>
                </div>   
                    
                <br><br>
                <h3 style='text-align: left;'>Вкладка 1. Рассчет сублимации. Формулы.</h3>
                <p><b>Формула температуры сублимации [K]:</b></p>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    T<sub>sub</sub>(r<sub>☉</sub>, r<sub>⊕</sub>) = 1.3 × 10<sup>3</sup> × ξ<sup>-1</sup> × (H / 3.2 × 10<sup>10</sup>) × (μ / 170) × (r<sub>☉</sub> / 1 a.e.)<sup>-1/2</sup> × (1 + 0.1 / (1 + (r<sub>⊕</sub> / R<sub>⊕</sub>)<sup>2</sup>)) <br>
                    где ξ = 1 + 0.02 × ln(P<sub>0</sub> / 6.7×10<sup>14</sup>), R<sub>⊕</sub> = 6371 км (радиус Земли)
                </div>

                <p><b>Суммарная температура:</b></p>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    T<sub>total</sub> = [ ( (1-A) × 1361 × r<sub>☉</sub><sup>-2</sup> / (4 × σ × ε) ) + ( 288<sup>4</sup> × (R<sub>⊕</sub> / r<sub>⊕</sub>)<sup>2</sup> × (1 + α)<sup>4</sup> ) ]<sup>1/4</sup> <br>
                    где A - альбедо частицы (0–1), σ = 5.67×10<sup>-8</sup> Вт/м<sup>2</sup>К<sup>4</sup> (постоянная Стефана-Больцмана), α ≈ 0.3 - доля отражённого Землёй света, R<sub>⊕</sub> = 6371 км (радиус Земли)
                </div>

                <p><b>Условие сублимации:</b></p>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    T<sub>total</sub> ≥ T<sub>sub</sub> <span style='font-size: 0.9em;'>и при r<sub>⊕</sub> ≤ 1.1 R<sub>⊕</sub></span>, P<sub>vap</sub>(T) > P<sub>атмосферы</sub>
                </div>

                <br><br>
                <h3 style='text-align: left;'>Вкладка 2. Графики.</h3>
                <p>Во вкладке доступны четыре типа графиков. Точки можно вводить вручную либо загружать из файла с двумя колонками (X и Y).</p>
                <ul style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    <li><i>Afρ от расстояния</i> — строится зависимость log(Afρ) от log(r).</li>
                    <li><i>Звездной величины от расстояния</i> — отображается m от log(r).</li>
                    <li><i>Afρ от даты</i> — график log(Afρ) во времени по датам вида YYYY-MM-DD.</li>
                    <li><i>Звездной величины от даты</i> — показывает изменение m со временем.</li>
                </ul>
                <p>Перед построением убедитесь, что списки X и Y содержат одинаковое количество значений.</p>

                <br><br>
                <h3 style='text-align: left;'>Вкладка 3. Рассчет массы, выделяемой кометой. Формула.</h3>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    N = 10<sup>-0.4×(m<sub>k</sub> - m<sub>ЛК</sub>)</sup> × Δ<sup>2</sup> × r<sup>2</sup> / (1.37×10<sup>-38</sup> × f(c<sub>2</sub>))<br>
                    где m<sub>ЛК</sub> = -13.78<sup>m</sup>, f(c<sub>2</sub>) = 0.031
                </div>

                <br><br>
                <h3 style='text-align: left;'>Вкладка 4. Рассчет диаметра ядра кометы. Формула.</h3>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    D = 1329 / √p<sub>v</sub> × 10<sup>-0.2×H</sup> <span style="font-size: 0.95em;">(диаметр ядра)</span>
                </div>                 
            </div>
        </div>
        """)
        content.setStyleSheet("""
            QLabel {
                background: transparent;
                color: white;
                border: none;
                padding: 20px;
            }
        """)
        content.setWordWrap(True)
        content.setAlignment(Qt.AlignJustify)
        
        content_layout.addWidget(content)
        scroll_area.setWidget(content_widget)
        inner_layout.addWidget(scroll_area, 1)
        
        self.close_btn = QPushButton("Спасибо!")
        self.close_btn.setFixedSize(750, 40)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 20px;
                color: #000034;
                font-size: 20px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #aaccff;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        inner_layout.addWidget(self.close_btn, 0, Qt.AlignBottom | Qt.AlignHCenter)

class SublimationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #0b0b47; border: none")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        params_frame = QFrame()
        params_frame.setStyleSheet("""
            QFrame {
                background-color: #0b0b47;
                border: 2px solid #aaaaaa;
                border-radius: 10px;
                padding: 2px;
            }
        """)
        params_layout = QVBoxLayout(params_frame)
        
        self.input_params = {
            'T': QLineEdit(),
            'r0': QLineEdit(),
            'r_earth': QLineEdit()
        }
        
        title_label = QLabel("Параметры для определения сублимирующих элементов:")
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
                color: white;
                border: none;
                padding: 5px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        params_layout.addWidget(title_label)
        
        param_label_style = """
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: white;
                border: 2px solid #aaaaaa;
                border-radius: 7px;
                padding: 5px;
                background-color: #0b0b47;
            }
        """
        
        params_layout.addWidget(self.create_param_row("Температура (T) [K]:", self.input_params['T'], param_label_style))
        params_layout.addWidget(self.create_param_row("Расстояние от звезды (r0) [а.е.]:", self.input_params['r0'], param_label_style))
        params_layout.addWidget(self.create_param_row("Расстояние от Земли (r⊕) [а.е.]:", self.input_params['r_earth'], param_label_style))
        
        layout.addWidget(params_frame)
        
        self.calc_btn = QPushButton("Определить сублимирующие элементы")
        self.calc_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 20px;
                color: #000034;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #aaccff;
            }
        """)
        layout.addWidget(self.calc_btn)
        
        self.result_label = QLabel("Результат:")
        self.result_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border-radius: 10px;
                color: #000034;
                font-family: Consolas;
            }
        """)
        layout.addWidget(self.result_text)
    
    def create_param_row(self, label_text, input_widget, label_style=""):
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
        
        input_widget.setFixedSize(150, 30)
        input_widget.setStyleSheet("""
            QLineEdit {
                background-color: #0b0b47;
                border: 2px solid #aaaaaa;
                border-radius: 5px;
                color: white;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:hover {
                border: 2px solid #5f8bff;
            }
            QLineEdit:focus {
                border: 2px solid #5f8bff;
            }
        """)
        
        row_layout.addWidget(label, 1)
        row_layout.addWidget(input_widget, 2)
        
        row_widget.label_widget = label
        row_widget.input_widget = input_widget

        return row_widget

class GraphWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("График")
        self.setMinimumSize(1100, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.background = QLabel(central_widget)
        self.background.setScaledContents(True)
        pixmap = QPixmap(resource_path("data/bg.jpeg"))
        if not pixmap.isNull():
            self.background.setPixmap(pixmap)
        else:
            self.background.setStyleSheet("background-color: #0b0b47;")
        self.background.setGeometry(0, 0, self.width(), self.height())
        self.background.lower()

        graph_container = QFrame()
        graph_container.setStyleSheet(
            """
            QFrame {
                background-color: #0b0b47;
                border-radius: 15px;
                border: 2px solid #aaaaaa;
            }
            """
        )
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(10, 10, 10, 10)

        self.figure = Figure(facecolor="#0b0b47")
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#0b0b47")

        self.ax.tick_params(colors="white")
        self.ax.xaxis.label.set_color("white")
        self.ax.yaxis.label.set_color("white")
        self.ax.title.set_color("white")

        self.toolbar = CustomNavigationToolbar(self.canvas, self)

        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)
        main_layout.addWidget(graph_container)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "background"):
            self.background.setGeometry(0, 0, self.width(), self.height())

class GraphTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph_window = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #0b0b47;")
        layout = QVBoxLayout(self)

        mpl.rcParams.update({
            'axes.labelcolor': 'white',
            'xtick.color': 'white',
            'ytick.color': 'white',
            'text.color': 'white',
            'axes.edgecolor': 'white',
            'figure.facecolor': '#0b0b47',
            'axes.facecolor': '#0b0b47',
            'savefig.facecolor': '#0b0b47',
            'figure.edgecolor': '#0b0b47',
            'toolbar': 'toolmanager',
            'keymap.save': '',
            'interactive': True,
            'figure.autolayout': True,
            'figure.edgecolor': '#0b0b47',
            'figure.subplot.left': 0.1,
            'figure.subplot.right': 0.9,
            'figure.subplot.bottom': 0.1,
            'figure.subplot.top': 0.9,
            'figure.subplot.wspace': 0.2,
            'figure.subplot.hspace': 0.2
        })

        graph_selector_layout = QHBoxLayout()
        graph_label = QLabel("Тип графика:")
        graph_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")

        self.graph_type = QComboBox()
        self.graph_types_list = [
            "Afρ от расстояния",
            "Звездной величины от расстояния",
            "Afρ от даты",
            "Звездной величины от даты",
        ]
        self.graph_type.addItems(self.graph_types_list)

        combo_view = QListView()
        combo_view.setStyleSheet("""
            QListView {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #5f8bff;
            }
            QListView::item:selected {
                background-color: #aaccff;
                color: #000034;
            }
        """)
        self.graph_type.setView(combo_view)
        self.graph_type.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #5f8bff;
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
                border-left: 2px solid #5f8bff;
                border-top-right-radius: 9px;
                border-bottom-right-radius: 9px;
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
            }
        """)

        graph_selector_layout.addWidget(graph_label)
        graph_selector_layout.addWidget(self.graph_type)
        graph_selector_layout.addStretch()
        layout.addLayout(graph_selector_layout)
        layout.addSpacing(10)

        params_frame = QFrame()
        params_frame.setStyleSheet("""
            QFrame {
                background-color: #0b0b47;
                border: 2px solid #aaaaaa;
                border-radius: 10px;
            }
        """)
        params_layout = QVBoxLayout(params_frame)

        self.graph_params = {
            'Afρ0': QLineEdit(),
            'r0': QLineEdit(),
            'k': QLineEdit(),
            'H': QLineEdit(),
            'n': QLineEdit(),
            'delta': QLineEdit(),
            'x_points': QLineEdit(),
            'y_points': QLineEdit(),
        }
        self.params_files = {
            "Afρ от расстояния": resource_path("data/params_afrho_r.json"),
            "Звездной величины от расстояния": resource_path("data/params_mag_r.json"),
            "Afρ от даты": resource_path("data/params_afrho_date.json"),
            "Звездной величины от даты": resource_path("data/params_mag_date.json"),
        }
        self.saved_params = {t: self._load_params(t) for t in self.graph_types_list}
        self.last_graph_type = self.graph_types_list[0]
        self.param_rows = {}
        self.param_labels = {}

        params_title = QLabel("Параметры для графиков:")
        params_title.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
                color: white;
                border: none;
                padding: 5px;
            }
        """)
        params_title.setAlignment(Qt.AlignCenter)
        params_layout.addWidget(params_title)

        param_label_style = """
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: white;
                border: 2px solid #aaaaaa;
                border-radius: 7px;
                padding: 5px;
                background-color: #0b0b47;
            }
        """

        self.param_rows['Afρ0'], self.param_labels['Afρ0'] = self.create_param_row("Afρ0:", self.graph_params['Afρ0'], param_label_style)
        params_layout.addWidget(self.param_rows['Afρ0'])

        self.param_rows['r0'], self.param_labels['r0'] = self.create_param_row("r0:", self.graph_params['r0'], param_label_style)
        params_layout.addWidget(self.param_rows['r0'])

        self.param_rows['k'], self.param_labels['k'] = self.create_param_row("k:", self.graph_params['k'], param_label_style)
        params_layout.addWidget(self.param_rows['k'])

        self.param_rows['H'], self.param_labels['H'] = self.create_param_row("Абсолютная звездная величина (H):", self.graph_params['H'], param_label_style)
        params_layout.addWidget(self.param_rows['H'])

        self.param_rows['n'], self.param_labels['n'] = self.create_param_row("Показатель n:", self.graph_params['n'], param_label_style)
        params_layout.addWidget(self.param_rows['n'])

        self.param_rows['delta'], self.param_labels['delta'] = self.create_param_row("Δ:", self.graph_params['delta'], param_label_style)
        params_layout.addWidget(self.param_rows['delta'])

        self.param_rows['x_points'], self.param_labels['x_points'] = self.create_param_row("Значения X (через пробел/запятую):", self.graph_params['x_points'], param_label_style)
        params_layout.addWidget(self.param_rows['x_points'])

        self.param_rows['y_points'], self.param_labels['y_points'] = self.create_param_row("Значения Y (через пробел/запятую):", self.graph_params['y_points'], param_label_style)
        params_layout.addWidget(self.param_rows['y_points'])

        self.load_points_btn = QPushButton("Загрузить точки из файла")
        self.load_points_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 15px;
                color: #000034;
                font-size: 14px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #aaccff;
            }
        """)
        params_layout.addWidget(self.load_points_btn)

        self.clear_points_btn = QPushButton("Очистить точки")
        self.clear_points_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 15px;
                color: #000034;
                font-size: 14px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #aaccff;
            }
        """)
        params_layout.addWidget(self.clear_points_btn)

        layout.addWidget(params_frame)

        self.graph_type.currentIndexChanged.connect(self.on_graph_type_changed)
        self.update_param_fields()
        saved = self.saved_params.get(self.last_graph_type, {})
        for k, w in self.graph_params.items():
            if k in saved:
                w.setText(saved[k])

        self.points_table = QTableWidget()
        self.points_table.setColumnCount(2)
        self.points_table.setHorizontalHeaderLabels(["X", "Y"])
        self.points_table.horizontalHeader().setStretchLastSection(True)
        self.points_table.setStyleSheet("background-color: white; color: #000034;")
        self.points_table.setMinimumHeight(150)
        layout.addWidget(self.points_table)

        self._update_points_table(saved.get('x_points', ''), saved.get('y_points', ''))

        self.plot_btn = QPushButton("Построить график")
        self.plot_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 20px;
                color: #000034;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #aaccff;
            }
        """)
        layout.addWidget(self.plot_btn)
    
    def create_param_row(self, label_text, input_widget, label_style=""):
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
        
        input_widget.setFixedSize(150, 30)
        input_widget.setStyleSheet("""
            QLineEdit {
                background-color: #0b0b47;
                border: 2px solid #aaaaaa;
                border-radius: 5px;
                color: white;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:hover {
                border: 2px solid #5f8bff;
            }
            QLineEdit:focus {
                border: 2px solid #5f8bff;
            }
        """)
        
        row_layout.addWidget(label, 1)
        row_layout.addWidget(input_widget, 2)
        
        row_widget.label_widget = label
        row_widget.input_widget = input_widget

        return row_widget, label
    
    def _parse_text(self, text: str):
        text = text.strip()
        if not text:
            return []
        if ',' in text and ' ' not in text:
            parts = text.split(',')
        else:
            parts = text.replace(',', ' ').split()
        return parts

    def _load_params(self, gtype):
        path = self.params_files.get(gtype)
        if path and os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_params(self, gtype, params):
        path = self.params_files.get(gtype)
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(params, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

    def _update_points_table(self, x_text, y_text):
        xs = self._parse_text(x_text)
        ys = self._parse_text(y_text)
        if xs and ys and len(xs) == len(ys):
            self.set_points(xs, ys)
        else:
            self.clear_points()
    
    def set_points(self, x_vals, y_vals):
        self.points_table.setRowCount(0)
        for xv, yv in zip(x_vals, y_vals):
            row = self.points_table.rowCount()
            self.points_table.insertRow(row)
            self.points_table.setItem(row, 0, QTableWidgetItem(str(xv)))
            self.points_table.setItem(row, 1, QTableWidgetItem(str(yv)))
        self.graph_params['x_points'].setText(' '.join(str(v) for v in x_vals))
        self.graph_params['y_points'].setText(' '.join(str(v) for v in y_vals))
        ctype = self.graph_type.currentText()
        self.saved_params[ctype] = {k: w.text() for k, w in self.graph_params.items()}
        self._save_params(ctype, self.saved_params[ctype])

    def clear_points(self):
        self.points_table.setRowCount(0)
        self.graph_params['x_points'].clear()
        self.graph_params['y_points'].clear()
        ctype = self.graph_type.currentText()
        self.saved_params[ctype] = {k: w.text() for k, w in self.graph_params.items()}
        self._save_params(ctype, self.saved_params[ctype])

    def get_point_texts(self):
        if self.points_table.rowCount() > 0:
            xs = []
            ys = []
            for row in range(self.points_table.rowCount()):
                x_item = self.points_table.item(row, 0)
                y_item = self.points_table.item(row, 1)
                if x_item and y_item:
                    xs.append(x_item.text())
                    ys.append(y_item.text())
            return ' '.join(xs), ' '.join(ys)
        return (
            self.graph_params['x_points'].text(),
            self.graph_params['y_points'].text(),
        )
    
    def on_graph_type_changed(self):
        self.saved_params[self.last_graph_type] = {
            k: w.text() for k, w in self.graph_params.items()
        }
        self._save_params(self.last_graph_type, self.saved_params[self.last_graph_type])
        new_type = self.graph_type.currentText()
        if new_type not in self.saved_params:
            self.saved_params[new_type] = self._load_params(new_type)
        saved = self.saved_params.get(new_type, {})
        for k, w in self.graph_params.items():
            if k in saved:
                w.setText(saved[k])
        self._update_points_table(saved.get('x_points', ''), saved.get('y_points', ''))
        self.last_graph_type = new_type
        self.update_param_fields()
    
    def update_param_fields(self):
        gtype = self.graph_type.currentText()
        # Hide all
        for row in self.param_rows.values():
            row.hide()

        if gtype == "Afρ от расстояния":
            self.param_labels['x_points'].setText("r (а.е.):")
            self.param_labels['y_points'].setText("Afρ:")
            self.param_rows['x_points'].show()
            self.param_rows['y_points'].show()
        elif gtype == "Звездной величины от расстояния":
            self.param_labels['x_points'].setText("Расстояние (pc):")
            self.param_labels['y_points'].setText("m:")
            self.param_rows['x_points'].show()
            self.param_rows['y_points'].show()
        elif gtype == "Afρ от даты":
            self.param_labels['x_points'].setText("Дата (YYYY-MM-DD):")
            self.param_labels['y_points'].setText("Afρ:")
            self.param_rows['x_points'].show()
            self.param_rows['y_points'].show()
        elif gtype == "Звездной величины от даты":
            self.param_labels['x_points'].setText("Дата (YYYY-MM-DD):")
            self.param_labels['y_points'].setText("m:")
            self.param_rows['x_points'].show()
            self.param_rows['y_points'].show()

class MassTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #0b0b47; border: none")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        params_frame = QFrame()
        params_frame.setStyleSheet("""
            QFrame {
                background-color: #0b0b47;
                border: 2px solid #aaaaaa;
                border-radius: 10px;
                padding: 2px;
            }
        """)
        params_layout = QVBoxLayout(params_frame)
        
        title_label = QLabel("Параметры для расчета массы пыли, выделяемую кометой:")
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
                color: white;
                border: none;
                padding: 5px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        params_layout.addWidget(title_label)
        
        param_label_style = """
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: white;
                border: 2px solid #aaaaaa;
                border-radius: 7px;
                padding: 5px;
                background-color: #0b0b47;
            }
        """
        
        self.mass_params = {
            'm_k': QLineEdit(),
            'delta': QLineEdit(),
            'r': QLineEdit()
        }
        
        params_layout.addWidget(self.create_param_row("Видимая звездная величина кометы (m_k):", 
                                                   self.mass_params['m_k'], param_label_style))
        params_layout.addWidget(self.create_param_row("Расстояние (Δ):", 
                                                   self.mass_params['delta'], param_label_style))
        params_layout.addWidget(self.create_param_row("Радиус (r):", 
                                                   self.mass_params['r'], param_label_style))
        
        layout.addWidget(params_frame)
        
        self.calc_btn = QPushButton("Рассчитать массу пыли, выделяемую кометой")
        self.calc_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 20px;
                color: #000034;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #aaccff;
            }
        """)
        layout.addWidget(self.calc_btn)
        
        self.result_label = QLabel("Результат:")
        self.result_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border-radius: 10px;
                color: #000034;
                font-family: Consolas;
            }
        """)
        layout.addWidget(self.result_text)
    
    def create_param_row(self, label_text, input_widget, label_style=""):
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
        
        input_widget.setFixedSize(150, 30)
        input_widget.setStyleSheet("""
            QLineEdit {
                background-color: #0b0b47;
                border: 2px solid #aaaaaa;
                border-radius: 5px;
                color: white;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:hover {
                border: 2px solid #5f8bff;
            }
            QLineEdit:focus {
                border: 2px solid #5f8bff;
            }
        """)
        
        row_layout.addWidget(label, 1)
        row_layout.addWidget(input_widget, 2)
        
        return row_widget

class SizeTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("background-color: #0b0b47; border: none")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        params_frame = QFrame()
        params_frame.setStyleSheet("""
            QFrame {
                background-color: #0b0b47;
                border: 2px solid #aaaaaa;
                border-radius: 10px;
                padding: 2px;
            }
        """)
        params_layout = QVBoxLayout(params_frame)
        
        self.size_params = {
            'H': QLineEdit(),
            'pv': QLineEdit(),
            'angular_size': QLineEdit()
        }
        
        title_label = QLabel("Параметры для расчета размера ядра:")
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
                color: white;
                border: none;
                padding: 5px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        params_layout.addWidget(title_label)
        
        param_label_style = """
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: white;
                border: 2px solid #aaaaaa;
                border-radius: 7px;
                padding: 5px;
                background-color: #0b0b47;
            }
        """
        
        params_layout.addWidget(self.create_param_row("Абсолютная звездная величина (H):", self.size_params['H'], param_label_style))
        params_layout.addWidget(self.create_param_row("Геометрическое альбедо (pv):", self.size_params['pv'], param_label_style))
        params_layout.addWidget(self.create_param_row("Угловой размер:", self.size_params['angular_size'], param_label_style))
        
        layout.addWidget(params_frame)
        
        self.calc_btn = QPushButton("Рассчитать размер ядра")
        self.calc_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 20px;
                color: #000034;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #aaccff;
            }
        """)
        layout.addWidget(self.calc_btn)
        
        self.result_label = QLabel("Результат:")
        self.result_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border-radius: 10px;
                color: #000034;
                font-family: Consolas;
            }
        """)
        layout.addWidget(self.result_text)
    
    def create_param_row(self, label_text, input_widget, label_style=""):
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
        
        input_widget.setFixedSize(150, 30)
        input_widget.setStyleSheet("""
            QLineEdit {
                background-color: #0b0b47;
                border: 2px solid #aaaaaa;
                border-radius: 5px;
                color: white;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:hover {
                border: 2px solid #5f8bff;
            }
            QLineEdit:focus {
                border: 2px solid #5f8bff;
            }
        """)
        
        row_layout.addWidget(label, 1)
        row_layout.addWidget(input_widget, 2)
        
        return row_widget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KUBSU Astro App")
        self.setMinimumSize(1100, 900)
        self.setup_ui()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.background = QLabel(central_widget)
        self.background.setScaledContents(True)

        pixmap = QPixmap(resource_path("data/bg.jpeg"))

        self.background.setPixmap(pixmap)
        self.background.setGeometry(0, 0, self.width(), self.height())
        self.background.lower()
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(70, 40, 70, 70)
        
        top_buttons = QHBoxLayout()
        top_buttons.setAlignment(Qt.AlignRight)

        self.load_btn = QPushButton("Загрузить данные")
        self.load_btn.setFixedSize(180, 40)
        self.load_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 50, 0.6);
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
        top_buttons.addWidget(self.help_btn)

        main_layout.addLayout(top_buttons)

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
        
        left_panel = QFrame()
        left_panel.setFixedWidth(158)
        left_panel.setStyleSheet("background-color: #0b0b47; border: none")
        content_layout.addWidget(left_panel)
        content_layout.addSpacing(15)
        
        nav_layout = QVBoxLayout(left_panel)
        nav_layout.setSpacing(30)
        nav_layout.addSpacing(55)
        
        self.nav_buttons = []
        buttons = [
            ("Сублимация", "sublimation"),
            ("Графики", "graphs"),
            ("Масса пыли", "mass"),
            ("Размер ядра", "size")
        ]

        for text, tab_name in buttons:
            btn = QPushButton(text)
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
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        nav_layout.addStretch()
        
        self.right_panel = QFrame()
        self.right_panel.setStyleSheet("background-color: #0b0b47; border: none")
        content_layout.addWidget(self.right_panel, 1)
        
        self.tabs = {
            "sublimation": SublimationTab(),
            "graphs": GraphTab(),
            "mass": MassTab(),
            "size": SizeTab()
        }
        
        self.right_layout = QVBoxLayout(self.right_panel)
        for tab in self.tabs.values():
            self.right_layout.addWidget(tab)
        
        self.show_tab("sublimation")
        self.update_nav_buttons("sublimation")
    
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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'background'):
            self.background.setGeometry(0, 0, self.width(), self.height())