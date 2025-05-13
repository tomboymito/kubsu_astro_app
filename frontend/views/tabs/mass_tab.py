from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, 
                            QFrame, QTextEdit)
from PyQt5.QtCore import Qt
from .base_tab import BaseTab

class MassTab(BaseTab):
    def init_ui(self):
        self.setStyleSheet("""background-color: #0b0b47; border: none""")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.init_input_fields(layout)
        self.init_calculate_button(layout)
        self.init_output_area(layout)

    def init_input_fields(self, layout):
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
        
        # Header
        row1 = QHBoxLayout()
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

        # Magnitude input
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
        
        # Distance input
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
        
        # Radius input
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

    def init_calculate_button(self, layout):
        self.calc_btn = QPushButton("Рассчитать")
        self.calc_btn.setCursor(Qt.PointingHandCursor)
        self.calc_btn.setFixedSize(519, 40)
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
        self.calc_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calc_btn)
        layout.addSpacing(10)

    def init_output_area(self, layout):
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

    import json
    import requests
    from frontend.views import BACKEND_API_URL

    def calculate(self):
        try:
            # Collect parameters from input fields
            magnitude = self.input1.text().strip()
            distance = self.input2.text().strip()
            radius = self.input3.text().strip()

            # Validate inputs (basic)
            if not magnitude or not distance or not radius:
                self.output_text.setPlainText("Пожалуйста, заполните все поля ввода.")
                return

            # Prepare parameters dict
            parameters = {
                "magnitude": float(magnitude),
                "distance": float(distance),
                "radius": float(radius)
            }

            # Prepare multipart/form-data payload
            files = {}
            data = {
                "calculation_type": "mass",
                "parameters": json.dumps(parameters)
            }

            # Send POST request to backend API
            response = requests.post(f"{BACKEND_API_URL}/calculate", data=data, files=files)

            if response.status_code == 200:
                result_json = response.json()
                if result_json.get("error") is None:
                    value = result_json.get("result")
                    units = result_json.get("units", "")
                    self.output_text.setPlainText(f"Результат: {value} {units}")
                else:
                    self.output_text.setPlainText(f"Ошибка: {result_json.get('error')}")
            else:
                self.output_text.setPlainText(f"Ошибка сервера: {response.status_code} {response.text}")

        except Exception as e:
            self.output_text.setPlainText(f"Ошибка при выполнении запроса: {str(e)}")
