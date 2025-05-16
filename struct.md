kubsu_astro_app/setup.py
```
from setuptools import setup, find_packages

setup(
    name="kubsu_astro_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15',
        'numpy>=1.24',
        'matplotlib>=3.7',
    ],
    entry_points={
        'gui_scripts': [
            'astro_app=application.frontend.front_v2:main',
        ],
    },
)
```

kubsu_astro_app/run_all.ps1
```
# PowerShell script to run backend and frontend concurrently with error handling
Start-Transcript -Path "logs/run_log.txt"
# run_all.ps1 - финальная версия с чистым выводом

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Создаем папку для логов
New-Item -ItemType Directory -Path logs -Force | Out-Null

Write-Host "=== Launching Application ==="

# Очистка порта
$processes = @(Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique)
if ($processes) {
    Write-Host "Found $($processes.Count) processes using port 8000:"
    $processes | ForEach-Object {
        $procName = (Get-Process -Id $_ -ErrorAction SilentlyContinue).ProcessName
        Write-Host " - Killing process $_ ($procName)"
        Stop-Process -Id $_ -Force
    }
    Start-Sleep -Seconds 2
}

# Запуск backend с логированием
Write-Host "Starting backend server (logs in logs/backend_*.log)..."
$backendJob = Start-Job -ScriptBlock {
    $env:PYTHONUNBUFFERED = "1"
    Set-Location $using:PWD
    & python -m uvicorn application.backend.main:app --port 8000 --host 0.0.0.0 1>logs/backend_out.log 2>logs/backend_error.log
}

# Ожидание с увеличенным таймаутом
Write-Host "Waiting for backend (20 sec max)..."
$attempts = 0
while ($attempts -lt 20) {
    $conn = Test-NetConnection -ComputerName localhost -Port 8000 -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($conn) {
        Write-Host "Backend ready on port 8000"
        break
    }
    $attempts++
    Start-Sleep -Seconds 1
    
    # Вывод прогресса
    if ($attempts % 5 -eq 0) {
        Write-Host "Waiting... ($attempts/20 seconds passed)"
    }
}

if ($attempts -ge 20) {
    Write-Host "Backend failed to start after 20 seconds" -ForegroundColor Red
    Write-Host "Check logs/backend_error.log for details" -ForegroundColor Yellow
    exit 1
}

# Запуск frontend
Write-Host "Starting frontend application..."
try {
    $frontendProcess = Start-Process -NoNewWindow -PassThru -FilePath "python" -ArgumentList "application/frontend/front_v2.py"
    Wait-Process -Id $frontendProcess.Id
    Write-Host "Frontend closed"
} finally {
    Write-Host "Stopping backend..."
    Stop-Job $backendJob
    Remove-Job $backendJob
    Receive-Job $backendJob | Out-Null
}

Write-Host "=== Application stopped ==="

Stop-Transcript
```

kubsu_astro_app/requirements.txt
```
PyQt5==5.15.9
numpy==1.24.3
matplotlib==3.7.1
```

kubsu_astro_app/conftest.py
```
import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
root = Path(__file__).parent
sys.path.insert(0, str(root))
```

kubsu_astro_app/application/main.py
```
from application.frontend.front_v2 import MainApplication
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())
```

kubsu_astro_app/application/__init__.py
```
# Package initializer for app
```

kubsu_astro_app/application/frontend/__init__.py
```
# Package initializer for frontend
```

kubsu_astro_app/application/frontend/requirements.txt
```
pyqt5
numpy
matplotlib
```

kubsu_astro_app/application/frontend/bg.jpeg

kubsu_astro_app/application/frontend/front_v2.jpeg
```
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

import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Поднимаемся на 1 уровень вверх
sys.path.append(project_root)

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
                <h3 style='text-align: left;'>Вкладка 2. Графики. Формулы.</h3>
                <p><b>Зависимость от расстояния:</b></p>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    Afρ(r<sub>☉</sub>) = Afρ<sub>0</sub> × (r<sub>☉</sub> / r<sub>0</sub>)<sup>k</sup> 
                </div>
                <p><b>Звездная величина:</b></p>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    m = H + 5 × log<sub>10</sub>(Δ) + 2.5 × n × log<sub>10</sub>(r<sub>☉</sub>)
                </div>
                <p><b>Временная зависимость:</b></p>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    Afρ(t) = Afρ<sub>peak</sub> × exp( - (t - t<sub>0</sub>)<sup>2</sup> / (2τ<sup>2</sup>) )
                </div>
                <p><b>Временная величина:</b></p>
                <div style='text-align: left; margin: 10px 0; line-height: 1.35;'>
                    m(t) = m<sub>0</sub> + 2.5 × β × log<sub>10</sub>(r<sub>☉</sub>(t) / r<sub>0</sub>)
                </div>



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
    
    def create_graph_tab(self):
        """Создает вкладку для графиков (из front_v1.py с адаптацией)"""
        tab = QWidget()
        tab.setStyleSheet("background-color: #0b0b47;")
        layout = QVBoxLayout(tab)
        
        # Графический селектор (из v1)
        graph_selector_layout = QHBoxLayout()
        graph_label = QLabel("Тип графика:")
        graph_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        
        self.graph_combo = QComboBox()
        self.graph_combo.addItems([
            "Afρ от расстояния", 
            "Звездной величины от расстояния",
            "Afρ от даты", 
            "Звездной величины от даты"
        ])
        
        # Стилизация комбобокса (из v1)
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
            /* Остальные стили из v1 */
        """)
        
        graph_selector_layout.addWidget(graph_label)
        graph_selector_layout.addWidget(self.graph_combo)
        layout.addLayout(graph_selector_layout)
        
        # Контейнер для графика
        graph_container = QFrame()
        graph_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: none;
            }
        """)
        
        # Matplotlib canvas
        self.figure = Figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#f8f8f8')
        
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.addWidget(self.canvas)
        layout.addWidget(graph_container, 1)
        
        return tab
    
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
            "graphs": self.create_graph_tab(),  # Используем новый метод
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
        
        # self.input1.setValidator(QDoubleValidator())  # Только числа

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
        
        # self.input1.setValidator(QDoubleValidator())  # Только числа

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
        
        # self.input1.setValidator(QDoubleValidator())  # Только числа

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
        """Загружает файл данных (.txt или .fits)"""
        from PyQt5.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл данных",
            "",
            "Текстовые файлы (*.txt);;FITS файлы (*.fits)"
        )
        
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    response = requests.post(
                        "http://localhost:8000/api/calculate",
                        files={"file": file},
                        data={"calculation_type": "sublimation"}  # Или другой тип
                    )
                    result = response.json()
                    self.output_text.setPlainText(str(result))
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def api_calculate(self, calculation_type, parameters):
        """Отправляет запрос к backend API"""
        url = "http://localhost:8000/api/calculate"
        try:
            response = requests.post(
                url,
                json={"calculation_type": calculation_type, "parameters": parameters},
                timeout=5  # Таймаут 5 секунд
            )
            response.raise_for_status()  # Проверка на HTTP-ошибки
            return response.json()
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self,
                "Ошибка API",
                f"Ошибка при запросе к backend:\n{str(e)}\n\nУбедитесь, что сервер запущен на localhost:8000"
            )
            return None

    def calculate_sublimation(self):
        """Обновленная версия с валидацией из v1"""
        try:
            if not all([self.input1.text(), self.input2.text(), self.input3.text()]):
                raise ValueError("Заполните все поля")
            # Получаем и проверяем значения
            temp = float(self.input1.text())
            earth_dist = float(self.input2.text())
            sun_dist = float(self.input3.text())
            
            if any(val <= 0 for val in [temp, earth_dist, sun_dist]):
                raise ValueError("Значения должны быть положительными")
                
            # Вызов API (как в v2)
            params = {
                "H": 5000,
                "Pb": 1.013e5,
                "P": temp,
                "mu": 18.0,
                "distance_earth": earth_dist,
                "distance_sun": sun_dist
            }
            
            result = self.api_calculate("sublimation", params)
            self.output_text.setPlainText(f"Результат: {result['value']} {result['units']}")
            
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректный ввод: {str(e)}")

    def calculate_mass(self):
        """Выполняет расчет массы"""
        try:
            # Проверяем, что поля не пустые
            if not all([self.input1.text(), self.input2.text(), self.input3.text()]):
                raise ValueError("Заполните все поля")
            
            m_k = float(self.input1.text())
            delta = float(self.input2.text())
            radius = float(self.input3.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, введите корректные числовые значения.")
            return
        
        params = {
            "m_k": m_k,          # Видимая звездная величина
            "m_sun": -26.74,     # Звездная величина Солнца
            "delta": delta,      # Геоцентрическое расстояние (а.е.)
            "r": radius,         # Гелиоцентрическое расстояние (а.е.)
            "f_C2": 1.0          # Поправочный коэффициент
        }

        result, units = self.api_calculate("mass", params)
        if result is not None:
            self.output_text.setPlainText(f"Результат: {result} {units}")
    
    def calculate_size(self):
        """Выполняет расчет размеров"""
        try:
            # Проверяем, что поля не пустые
            if not all([self.input1.text(), self.input2.text(), self.input3.text()]):
                raise ValueError("Заполните все поля")
        
            H = float(self.input1.text())
            p = float(self.input2.text())
            angular_size = float(self.input3.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, введите корректные числовые значения.")
            return
        
        params = {
            "A": angular_size,   # Проекционная площадь (км²)
            "p": p,              # Альбедо (0.04 по умолчанию)
            "H": H               # Абсолютная звездная величина
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
```

kubsu_astro_app/application/backend/setup.py
```
from setuptools import setup, find_packages

setup(
    name="astro_app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic',
        'numpy',
        'astropy',
        'scipy',
        'pandas',
        'python-multipart',
        'python-dotenv',
        'pytest',
        'pytest-cov',
        'locust'
    ],
)
```

kubsu_astro_app/application/backend/requirements.txt
```
fastapi==0.95.2
uvicorn==0.22.0
pydantic==1.10.7
numpy==1.24.3
astropy==5.2.2
scipy==1.10.1
pandas==2.0.1
python-multipart==0.0.6
python-dotenv==1.0.0
pytest==7.3.1
pytest-cov==4.0.0
locust==2.15.1
```

kubsu_astro_app/application/backend/main.py
```
import sys
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from application.backend.app.api.endpoints import router as api_router  # Измененный импорт
from application.backend.app.core.services.logger import setup_logger   # Измененный импорт

# Добавляем директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(
    title="Astronomy Comet Analysis API",
    description="API for astronomical calculations related to comets",
    version="1.0.0",
)

# Инициализация логгера
setup_logger()

# Подключение роутера API
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return JSONResponse(
        content={"message": "Astronomy Comet Analysis API is running"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

kubsu_astro_app/application/backend/.gitmodules
```
[submodule "cpp/pybind11"]
	path = cpp/pybind11
	url = https://github.com/pybind/pybind11.git\
```

kubsu_astro_app/application/backend/__init__.py
```
```

kubsu_astro_app/application/backend/tests/__init__.py
```
```

kubsu_astro_app/application/backend/tests/test_sublimation.py
```
import pytest
from application.backend.app.core.calculations.sublimation import calculate

def test_sublimation_calculation():
    """Тест расчета сублимации с корректными параметрами"""
    params = {
        "H": 5000.0,
        "Pb": 1.013e5,
        "P": 1.0,
        "mu": 18.0
    }
    result = calculate(None, params)
    
    assert isinstance(result["value"], float)
    assert result["units"] == "K"
    assert isinstance(result["composition"], str)
    assert 100 < result["value"] < 300

def test_sublimation_missing_params():
    """Тест с отсутствующими параметрами"""
    params = {
        "H": 5000.0,
        "Pb": 1.013e5
    }
    with pytest.raises(ValueError):
        calculate(None, params)

def test_sublimation_invalid_params():
    """Тест с недопустимыми параметрами"""
    params = {
        "H": -5000.0,  # Отрицательное значение
        "Pb": 1.013e5,
        "P": 1.0,
        "mu": 18.0
    }
    with pytest.raises(Exception):
        calculate(None, params)
```

kubsu_astro_app/application/backend/cpp/CMakeLists.txt
```
cmake_minimum_required(VERSION 3.15)
project(comet_calculations VERSION 1.0.0)

# Правильный путь к папке назначения (теперь внутри backend)
set(OUTPUT_DIR "${CMAKE_SOURCE_DIR}/../app/core/calculations")
file(MAKE_DIRECTORY ${OUTPUT_DIR})

# Настройка вывода для Visual Studio
if(MSVC)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${OUTPUT_DIR})
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${OUTPUT_DIR})
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_DIR})
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${OUTPUT_DIR})
endif()

add_subdirectory(pybind11)
find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter Development)

set(SOURCES
    core/sublimation.cpp
    core/mass.cpp
    core/nucleus.cpp
)

pybind11_add_module(comet_calculations ${SOURCES})

target_include_directories(comet_calculations PRIVATE
    ${PROJECT_SOURCE_DIR}/include
    ${Python3_INCLUDE_DIRS}
)

if(WIN32)
    set_target_properties(comet_calculations PROPERTIES
        SUFFIX ".pyd"
        PREFIX ""
    )
endif()

target_link_libraries(comet_calculations PRIVATE ${Python3_LIBRARIES})

message(STATUS "Output will be directed to: ${OUTPUT_DIR}")
```

kubsu_astro_app/application/backend/cpp/include/mass.h
```
#ifndef MASS_H
#define MASS_H

namespace comet {

class MassCalculator {
public:
    static double calculate_mass(double m_k, double m_sun, double delta, double r, double f_C2);
};

} // namespace comet

#endif // MASS_H
```

kubsu_astro_app/application/backend/cpp/include/nucleus.h
```
#ifndef NUCLEUS_H
#define NUCLEUS_H

namespace comet {

class NucleusCalculator {
public:
    static double calculate_diameter(double A, double p, double H);
};

} // namespace comet

#endif // NUCLEUS_H
```

kubsu_astro_app/application/backend/cpp/include/sublimation.h
```
#ifndef SUBLIMATION_H
#define SUBLIMATION_H

#include <string>

namespace comet {

class SublimationCalculator {
public:
    static double calculate_temperature(double H, double P0, double P, double mu);
    static std::string estimate_composition(double temperature);
};

} // namespace comet

#endif // SUBLIMATION_H
```

kubsu_astro_app/application/backend/cpp/core/mass.cpp
```
#include "../include/mass.h"
#include <stdexcept>
#include <cmath>

namespace comet {

double MassCalculator::calculate_mass(double m_k, double m_sun, double delta, double r, double f_C2) {
    // Проверка параметров
    if (delta <= 0 || r <= 0 || f_C2 <= 0) {
        throw std::invalid_argument("Delta, r and f_C2 must be positive");
    }

    // Расчет числителя: 10^(-0.4*(m_k - m_sun)) * delta^2 * r^2
    double term1 = std::pow(10, -0.4 * (m_k - m_sun));
    double term2 = delta * delta * r * r;
    double numerator = term1 * term2;

    // Расчет знаменателя: 1.37e-38 * f_C2
    double denominator = 1.37e-38 * f_C2;
    
    if (denominator == 0) {
        throw std::runtime_error("Denominator in mass calculation is zero");
    }

    return numerator / denominator;
}

} // namespace comet
```

kubsu_astro_app/application/backend/cpp/core/nucleus.cpp
```
#include "../include/nucleus.h"
#include <stdexcept>
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

namespace comet {

double NucleusCalculator::calculate_diameter(double A, double p, double H) {
    if (A <= 0 || p <= 0 || H <= 0) {
        throw std::invalid_argument("Parameters must be positive");
    }
    // Формула: D = q * 4A / (π p H)
    // В ТЗ q не определён, предположим q = 1 для упрощения
    const double q = 1.0;
    return q * 4.0 * A / (M_PI * p * H);
}

} // namespace comet
```

kubsu_astro_app/application/backend/cpp/core/sublimation.cpp
```
#include "../include/sublimation.h"
#include <cmath>
#include <stdexcept>
#include <string>
#include <sstream>


namespace comet {


double SublimationCalculator::calculate_temperature(double H, double P0, double P, double mu) {
    if (P0 <= 0 || P <= 0 || mu <= 0) {
        throw std::invalid_argument("Pressure and mu must be positive");
    }
    double denominator = std::log(P0) - std::log(P) + std::log(mu);
    if (denominator == 0) {
        throw std::runtime_error("Denominator in temperature calculation is zero");
    }
    return H / denominator;
}


std::string SublimationCalculator::estimate_composition(double temperature) {
    if (temperature < 50) {
        return "CO, CO2, N2 (Volatile ices)";
    } else if (temperature < 150) {
        return "H2O (Water ice)";
    } else {
        return "Silicates, metals (Refractory materials)";
    }
}


} // namespace comet
```

kubsu_astro_app/application/backend/app/__init__.py
```
```

kubsu_astro_app/application/backend/app/api/__init__.py
```
```

kubsu_astro_app/application/backend/app/api/endpoints.py
```
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError  # Добавлен импорт BaseModel
from typing import Optional, Literal, Dict, Any
from application.backend.app.core.services.file_parser import parse_file  # Обновленный импорт
from application.backend.app.core.calculations import (
    sublimation,
    mass,
    nucleus,
)
import json
import logging

router = APIRouter(
    prefix="/api",
    tags=["calculations"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)

class CalculationRequest(BaseModel):
    """Схема запроса для расчетов"""
    calculation_type: Literal["sublimation", "mass", "nucleus"]
    parameters: Dict[str, Any]
    file_data: Optional[Dict] = None

class CalculationResponse(BaseModel):
    """Схема ответа с результатами расчета"""
    result: Any
    units: Optional[str] = None
    error: Optional[str] = None

@router.post("/calculate",
             summary="Выполнить астрономический расчет",
             response_model=CalculationResponse)
async def calculate_comet_data(
    file: Optional[UploadFile] = File(None),
    calculation_type: str = Form(...),
    parameters: Optional[str] = Form(None),
):
    """Выполняет один из доступных астрономических расчетов"""
    try:
        # Проверка наличия входных данных
        if not file and not parameters:
            raise HTTPException(
                status_code=400,
                detail="Either file or parameters must be provided"
            )

        # Парсинг параметров
        params_dict = {}
        if parameters:
            try:
                params_dict = json.loads(parameters)
                if not isinstance(params_dict, dict):
                    raise ValueError("Parameters must be a JSON object")
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid parameters JSON: {str(e)}"
                )

        # Парсинг файла
        file_data = None
        if file:
            if not file.filename:
                raise HTTPException(
                    status_code=400,
                    detail="Uploaded file must have a filename"
                )
            file_data = await parse_file(file)

        # Валидация запроса
        try:
            request_data = CalculationRequest(
                calculation_type=calculation_type,
                parameters=params_dict,
                file_data=file_data,
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=422,
                detail=e.errors()
            )

        # Выполнение расчета
        try:
            if request_data.calculation_type == "sublimation":
                result = sublimation.calculate(
                    request_data.file_data, request_data.parameters
                )
            elif request_data.calculation_type == "mass":
                result = mass.calculate(
                    request_data.file_data, request_data.parameters
                )
            elif request_data.calculation_type == "nucleus":
                result = nucleus.calculate(
                    request_data.file_data, request_data.parameters
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid calculation type"
                )

            return {
                "result": result.get("value"),
                "units": result.get("units", ""),
                "error": None,
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Calculation error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
```

kubsu_astro_app/application/backend/app/api/schemas.py
```
from pydantic import BaseModel
from typing import Optional, Dict, Any, Literal


class CalculationRequest(BaseModel):
    calculation_type: Literal["sublimation", "mass", "nucleus"]
    parameters: Dict[str, Any]
    file_data: Optional[Dict] = None


class CalculationResponse(BaseModel):
    result: Any
    units: Optional[str] = None
    error: Optional[str] = None


class PlotDataResponse(BaseModel):
    x: list
    y: list
    labels: Optional[Dict[str, Any]] = None
```

kubsu_astro_app/application/backend/app/core/__init__.py
```
```

kubsu_astro_app/application/backend/app/core/calculations/__init__.py
```
```

kubsu_astro_app/application/backend/app/core/calculations/cpp_loader.py
```
import ctypes
import platform
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)

class CppLoader:
    def __init__(self):
        self._lib = None
        self._lib_ext = {
            "Windows": ".pyd",
            "Linux": ".so",
            "Darwin": ".so"
        }.get(platform.system(), ".so")

    def load_library(self, lib_path: str) -> bool:
        """Загружает библиотеку по полному пути"""
        try:
            lib_path = str(Path(lib_path).with_suffix(self._lib_ext))
            self._lib = ctypes.CDLL(lib_path)
            logger.info(f"Successfully loaded library: {lib_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load library: {str(e)}")
            self._lib = None
            return False

    def print_exported_functions(self):
        if not self._lib:
            print("Library not loaded")
            return
        
        print("Exported functions:")
        for name in dir(self._lib):
            if not name.startswith('_'):
                print(f"- {name}")

    def get_function(self, func_name: str, argtypes: list, restype):
        """Получает функцию из загруженной библиотеки с проверками"""
        if not self._lib:
            raise RuntimeError("Library not loaded")

        func = getattr(self._lib, func_name, None)
        if not func:
            raise AttributeError(f"Function {func_name} not found in library")

        try:
            func.argtypes = argtypes
            func.restype = restype
            return func
        except Exception as e:
            logger.error(f"Failed to configure function {func_name}: {str(e)}")
            raise

# Инициализация загрузчика
cpp_loader = CppLoader()
```

kubsu_astro_app/application/backend/app/core/calculations/fake_cpp.py
```
class FakeCppLoader:
    def get_function(self, name, argtypes, restype):
        if name == 'calculate_temperature':
            return lambda H, Pb, P, mu: 42.0  # Заглушка
        raise AttributeError(f"Function {name} not found")

cpp_loader = FakeCppLoader()
```

kubsu_astro_app/application/backend/app/core/calculation/mass.py
```
import numpy as np
from typing import Dict, Any
import logging


logger = logging.getLogger(__name__)


def calculate_mass(
    m_k: float,
    m_sun: float,
    delta: float,
    r: float,
    f_C2: float = 1.0,
) -> float:
    # Исправлено: разбивка длинной строки функции для соответствия Flake8 E501
    """
    Расчет массы кометы по формуле:
    N = 10^(-0.4*(m_k - m_sun)) * delta^2 * r^2 / \
        (1.37e-38 * f(C2))
    """
    try:
        term1 = 10 ** (-0.4 * (m_k - m_sun))
        term2 = delta ** 2 * r ** 2
        denominator = 1.37e-38 * f_C2

        if denominator == 0:
            raise ValueError("Denominator in mass formula equals zero")

        mass = term1 * term2 / denominator
        return mass
    except Exception as e:
        logger.error(f"Error in mass calculation: {str(e)}")
        raise


def calculate(file_data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Основная функция расчета массы кометы"""
    try:
        # Проверка
        # наличия данных
        if file_data is None or "magnitude" not in file_data:
            raise ValueError("Missing magnitude data in input file")

        # Параметры по умолчанию
        default_params = {
            # Звездная величина Солнца
            "m_sun": -26.74,
            # Геоцентрическое расстояние [а.е.]
            "delta": 1.0,
            # Гелиоцентрическое расстояние [а.е.]
            "r": 1.0,
            # Поправочный коэффициент для C2
            "f_C2": 1.0,
        }

        # Обновление параметров пользовательскими значениями
        params = {**default_params, **parameters}

        # Используем среднюю звездную величину из данных
        m_k = np.mean(file_data["magnitude"])

        # Расчет массы
        mass = calculate_mass(m_k, params["m_sun"], params["delta"], params["r"], params["f_C2"])

        return {
            "value": mass,
            "units": "kg",
            "method": "photometric",
        }
    except Exception as e:
        logger.error(f"Mass calculation failed: {str(e)}")
        raise
```

kubsu_astro_app/application/backend/app/core/calculation/nucleus.py
```
from math import sqrt, pi
from typing import Dict, Any
import logging


logger = logging.getLogger(__name__)


def calculate_diameter(
    A: float,
    p: float,
    H: float,
) -> float:
    """Расчет диаметра ядра кометы по формуле: D = sqrt(4*A / (π*p*H))"""
    try:
        if p <= 0 or H <= 0:
            raise ValueError(
                "Albedo (p) and absolute "
                "magnitude (H) must be positive"
            )
            
        diameter = sqrt(4 * A / (pi * p * H))
        return diameter
    except Exception as e:
        logger.error(f"Error in nucleus diameter calculation: {str(e)}")
        raise


def calculate(
    file_data: Dict[str, Any],
    parameters: Dict[str, Any],
) -> Dict[str, Any]:
    """Основная функция расчета размера ядра кометы"""
    try:
        # Проверка наличия необходимых параметров
        if "A" not in parameters:
            raise ValueError("Missing parameter 'A' (projected area)")
        
        # Параметры по умолчанию
        default_params = {
            "p": 0.04,  # Альбедо (типичное значение для комет)
            "H": 18.0,  # Абсолютная звездная величина
        }
        
        # Обновление параметров пользовательскими значениями
        params = {**default_params, **parameters}
        
        # Расчет диаметра
        diameter = calculate_diameter(
            parameters["A"],
            params["p"],
            params["H"],
        )
        
        return {
            "value": diameter,
            "units": "km",
            "albedo": params["p"],
        }
    except Exception as e:
        logger.error(f"Nucleus diameter calculation failed: {str(e)}")
        raise
```

kubsu_astro_app/application/backend/app/core/calculations/sublimation.py
```
import ctypes
import logging
from pathlib import Path
from typing import Dict, Any  # Добавлен импорт типов
try:
    from .cpp_loader import cpp_loader
except ImportError:
    from .fake_cpp import cpp_loader  # Используем заглушку

logger = logging.getLogger(__name__)

# Путь к библиотеке относительно текущего файла
lib_dir = Path(__file__).parent
dll_path = lib_dir / "comet_calculations.pyd"

if not dll_path.exists():
    raise ImportError(f"Library not found at: {dll_path}. Please build C++ module first.")

# Загружаем библиотеку
if not cpp_loader.load_library(str(dll_path)):
    raise ImportError(f"Failed to load comet_calculations library from {dll_path}")

def calculate(file_data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Основная функция расчета сублимации"""
    try:
        required_params = ["H", "Pb", "P", "mu"]
        missing = [p for p in required_params if p not in parameters]
        if missing:
            raise ValueError(f"Missing required parameters: {missing}")

        # Получаем функцию из C++ библиотеки
        calculate_temp = cpp_loader.get_function(
            "calculate_temperature",
            [ctypes.c_double]*4,
            ctypes.c_double
        )
        
        temp = calculate_temp(
            parameters["H"],
            parameters["Pb"],
            parameters["P"],
            parameters["mu"]
        )
        
        estimate_comp = cpp_loader.get_function(
            "estimate_composition",
            [ctypes.c_double],
            ctypes.c_char_p
        )
        composition = estimate_comp(temp).decode('utf-8')
        
        return {
            "value": temp,
            "units": "K",
            "composition": composition
        }
    except Exception as e:
        logger.error(f"Sublimation calculation failed: {str(e)}")
        raise
```

kubsu_astro_app/application/backend/app/core/services/__init__.py
```
```

kubsu_astro_app/application/backend/app/core/services/config.py
```
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Astronomy Comet Analysis API"
    log_level: str = "DEBUG"
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()
```

kubsu_astro_app/application/backend/app/core/services/file_parser.py
```
from fastapi import UploadFile, HTTPException
from astropy.io import fits
import numpy as np
import pandas as pd
from typing import Dict, Union
import logging
import tempfile
from io import StringIO

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def parse_txt(file_content: str) -> Dict[str, np.ndarray]:
    """Парсит текстовый файл с данными кометы"""
    try:
        # Чтение данных через StringIO
        data = pd.read_csv(StringIO(file_content), delim_whitespace=True, comment='#')
        
        # Проверка на пустые данные
        if data.empty:
            raise ValueError("File contains no data")

        # Проверка обязательных колонок
        required_columns = {
            "Дни_до_перигелия": "days_to_perihelion",
            "Звёздная_величина": "magnitude",
            "Afrho": "afrho"
        }

        missing_cols = [col for col in required_columns if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        # Конвертация данных
        return {
            "days_to_perihelion": data["Дни_до_перигелия"].values.astype(float),
            "magnitude": data["Звёздная_величина"].values.astype(float),
            "afrho": data["Afrho"].values.astype(float)
        }
    except Exception as e:
        logger.error(f"Error parsing TXT file: {str(e)}")
        raise ValueError(f"TXT file parsing error: {str(e)}")

def parse_fits(file_path: str) -> Dict[str, np.ndarray]:
    """Парсит FITS файл с данными кометы"""
    try:
        with fits.open(file_path) as hdul:
            if len(hdul) < 2:
                raise ValueError("FITS file must contain at least 2 HDUs")

            data = hdul[1].data
            
            # Проверка обязательных полей
            required_fields = ["Days_to_Perihelion", "Magnitude", "Afrho"]
            missing_fields = [field for field in required_fields if field not in data.names]
            
            if missing_fields:
                raise ValueError(f"Missing required fields in FITS: {', '.join(missing_fields)}")

            return {
                "days_to_perihelion": data["Days_to_Perihelion"].astype(float),
                "magnitude": data["Magnitude"].astype(float),
                "afrho": data["Afrho"].astype(float)
            }
    except Exception as e:
        logger.error(f"Error parsing FITS file: {str(e)}")
        raise ValueError(f"FITS file parsing error: {str(e)}")

async def parse_file(file: UploadFile) -> Dict[str, Union[np.ndarray, list]]:
    """Основная функция парсинга файлов"""
    try:
        # Проверка размера файла
        if file.size > MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds maximum limit of {MAX_FILE_SIZE//(1024*1024)} MB")

        content = await file.read()
        
        if not content:
            raise ValueError("Uploaded file is empty")

        # Определение типа файла и парсинг
        if file.filename.endswith('.txt'):
            return parse_txt(content.decode('utf-8'))
        elif file.filename.endswith('.fits'):
            with tempfile.NamedTemporaryFile(delete=True) as tmp:
                tmp.write(content)
                tmp.flush()
                return parse_fits(tmp.name)
        else:
            raise ValueError(
                f"Unsupported file format: {file.filename.split('.')[-1]}. "
                "Supported formats: .txt, .fits"
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"File parsing failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during file parsing"
        )
```

kubsu_astro_app/application/backend/app/core/services/logger.py
```
import logging
import logging.config
from pathlib import Path
from datetime import datetime

def setup_logger():
    """Настройка системы логирования"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"error_{datetime.now().strftime('%Y%m%d')}.log"

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "%(levelname)s %(message)s"
            }
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": log_file,
                "level": "ERROR",
                "formatter": "detailed"
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple"
            }
        },
        "loggers": {
            "": {
                "handlers": ["file", "console"],
                "level": "DEBUG"
            }
        }
    })

    # Логирование успешной настройки
    logger = logging.getLogger(__name__)
    logger.info("Logging system has been initialized")
```