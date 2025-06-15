from PyQt5.QtWidgets import QFileDialog, QMessageBox
from point_manager import PointManager
from views import GraphWindow
from astropy.io import fits
import numpy as np

class MainController:
    def __init__(self, models, view):
        self.models = models
        self.view = view
        self.point_manager = PointManager()
        self.connect_signals()
        self.data = {}
    
    def connect_signals(self):
        # Подключение кнопок навигации
        for btn in self.view.nav_buttons:
            btn.clicked.connect(lambda checked, tn=btn.property('tab_name'): self.view.show_tab(tn))
        
        # Подключение кнопки загрузки данных
        self.view.load_btn.clicked.connect(self.load_data)
        
        # Подключение кнопки справки
        self.view.help_btn.clicked.connect(self.view.show_help)
        
        # Подключение кнопок расчета для каждой вкладки
        self.view.tabs["sublimation"].calc_btn.clicked.connect(self.calculate_sublimation)
        self.view.tabs["graphs"].plot_btn.clicked.connect(self.plot_graph)
        self.view.tabs["graphs"].load_points_btn.clicked.connect(self.load_points)
        self.view.tabs["mass"].calc_btn.clicked.connect(self.calculate_mass)
        self.view.tabs["size"].calc_btn.clicked.connect(self.calculate_size)
    
    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, "Открыть файл данных", "", 
            "Текстовые файлы (*.txt);;FITS файлы (*.fits)"
        )
        
        if not file_path:
            return
            
        try:
            if file_path.endswith('.txt'):
                self.models['sublimation'].load_txt_data(file_path)
                self.data = self.models['sublimation'].data
            elif file_path.endswith('.fits'):
                self.models['sublimation'].load_fits_data(file_path)
                self.data = self.models['sublimation'].data
                
            self.update_ui_with_data()
            QMessageBox.information(self.view, "Успех", "Данные успешно загружены!")
        except Exception as e:
            QMessageBox.critical(self.view, "Ошибка", f"Не удалось загрузить данные: {str(e)}")
    
    def update_ui_with_data(self):
        # Вкладка "Сублимация"
        if 'T' in self.data:
            self.view.tabs["sublimation"].input_params['T'].setText(str(self.data['T']))
        if 'r0' in self.data:
            self.view.tabs["sublimation"].input_params['r0'].setText(str(self.data['r0']))
        if 'r_earth' in self.data:
            self.view.tabs["sublimation"].input_params['r_earth'].setText(str(self.data['r_earth']))

        # Вкладка "Графики"
        if 'Afρ0' in self.data:
            self.view.tabs["graphs"].graph_params['Afρ0'].setText(str(self.data['Afρ0']))
        if 'r0' in self.data:
            self.view.tabs["graphs"].graph_params['r0'].setText(str(self.data['r0']))
        if 'k' in self.data:
            self.view.tabs["graphs"].graph_params['k'].setText(str(self.data['k']))
        if 'H' in self.data:
            self.view.tabs["graphs"].graph_params['H'].setText(str(self.data['H']))
        if 'n' in self.data:
            self.view.tabs["graphs"].graph_params['n'].setText(str(self.data['n']))
        if 'delta' in self.data:
            self.view.tabs["graphs"].graph_params['delta'].setText(str(self.data['delta']))
        
        # Вкладка "Масса пыли"
        if 'm_k' in self.data:
            self.view.tabs["mass"].mass_params['m_k'].setText(str(self.data['m_k']))
        if 'delta' in self.data:
            self.view.tabs["mass"].mass_params['delta'].setText(str(self.data['delta']))
        if 'r' in self.data:
            self.view.tabs["mass"].mass_params['r'].setText(str(self.data['r']))

        # Вкладка "Размер ядра"
        if 'H' in self.data:
            self.view.tabs["size"].size_params['H'].setText(str(self.data['H']))
        if 'pv' in self.data:
            self.view.tabs["size"].size_params['pv'].setText(str(self.data['pv']))
        if 'angular_size' in self.data:
            self.view.tabs["size"].size_params['angular_size'].setText(str(self.data['angular_size']))
    
    def calculate_sublimation(self):
        tab = self.view.tabs["sublimation"]
        input_params = {
            'T': tab.input_params['T'].text(),
            'r0': tab.input_params['r0'].text(),
            'r_earth': tab.input_params['r_earth'].text()
        }
        
        result = self.models['sublimation'].calculate_sublimation(input_params)
        
        if 'error' in result:
            QMessageBox.warning(self.view, "Ошибка", result['error'])
        else:
            tab.result_text.setPlainText(result['result'])
    
    def plot_graph(self):
        tab = self.view.tabs["graphs"]
        x_text, y_text = tab.get_point_texts()

        graph_type = tab.graph_type.currentText()

        params = {}

        if graph_type in ("Afρ от даты", "Звездной величины от даты"):
            x_parts = self.point_manager._parse_text(x_text)
            y_parts = self.point_manager._parse_text(y_text)
            if not x_parts or not y_parts:
                QMessageBox.warning(self.view, "Ошибка", "Нужно задать списки X и Y")
                return
            if len(x_parts) != len(y_parts) or len(x_parts) < 2:
                QMessageBox.warning(self.view, "Ошибка", "Количество точек X и Y должно совпадать и быть не менее двух")
                return
            try:
                params['x_vals'] = x_parts
                params['y_vals'] = np.array([float(v) for v in y_parts])
            except ValueError:
                QMessageBox.warning(self.view, "Ошибка", "Точки Y должны быть числами")
                return
        else:
            ok, msg = self.point_manager.validate_points(x_text, y_text)
            if ok:
                params['x_vals'] = self.point_manager.x
                params['y_vals'] = self.point_manager.y
            else:
                QMessageBox.warning(self.view, "Ошибка", msg)
                return
        
        result = self.models['graph'].plot_graph(params, graph_type)
        
        if 'error' in result:
            QMessageBox.warning(self.view, "Ошибка", result['error'])
        else:
            window = GraphWindow(self.view)
            window.ax.clear()
            window.ax.plot(result['x'], result['y'], color="blue")
            if result.get('points'):
                window.ax.scatter(result['x'], result['y'], color="red", zorder=3)
            window.ax.set_xlabel(result['xlabel'])
            window.ax.set_ylabel(result['ylabel'])
            window.ax.set_title(result['title'])
            if result['invert_y']:
                window.ax.invert_yaxis()
            window.canvas.draw()
            window.show()
    
    def load_points(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, "Открыть файл с точками", "", "Text/CSV Files (*.txt *.csv)"
        )
        if not file_path:
            return
        tab = self.view.tabs["graphs"]
        graph_type = tab.graph_type.currentText()
        if graph_type in ("Afρ от даты", "Звездной величины от даты"):
            x_vals = []
            y_vals = []
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().replace(";", " ").replace(",", " ").split()
                    if len(parts) >= 2:
                        x_vals.append(parts[0])
                        try:
                            y_vals.append(float(parts[1]))
                        except ValueError:
                            continue
            if len(x_vals) < 2 or len(x_vals) != len(y_vals):
                QMessageBox.warning(self.view, "Ошибка", "Некорректные данные в файле")
                return
            tab.set_points(x_vals, y_vals)
            self.point_manager.x = np.array(x_vals)
            self.point_manager.y = np.array(y_vals)
        else:
            ok, msg = self.point_manager.load_from_file(file_path)
            if not ok:
                QMessageBox.warning(self.view, "Ошибка", msg)
                return
            tab.set_points(self.point_manager.x, self.point_manager.y)

    def calculate_mass(self):
        tab = self.view.tabs["mass"]
        params = {
            'm_k': tab.mass_params['m_k'].text(),
            'delta': tab.mass_params['delta'].text(),
            'r': tab.mass_params['r'].text()
        }
        
        result = self.models['mass'].calculate_mass(params)
        
        if 'error' in result:
            QMessageBox.warning(self.view, "Ошибка", result['error'])
        else:
            tab.result_text.setPlainText(result['result'])
    
    def calculate_size(self):
        tab = self.view.tabs["size"]
        params = {
            'H': tab.size_params['H'].text(),
            'pv': tab.size_params['pv'].text(),
            'angular_size': tab.size_params['angular_size'].text()
        }
        
        result = self.models['size'].calculate_size(params)
        
        if 'error' in result:
            QMessageBox.warning(self.view, "Ошибка", result['error'])
        else:
            tab.result_text.setPlainText(result['result'])