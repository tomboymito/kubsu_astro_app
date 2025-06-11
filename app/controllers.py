from PyQt5.QtWidgets import QFileDialog, QMessageBox
from point_manager import PointManager
from astropy.io import fits

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
        ok, msg = self.point_manager.validate_points(x_text, y_text)
        params = {
            'Afρ0': tab.graph_params['Afρ0'].text(),
            'r0': tab.graph_params['r0'].text(),
            'k': tab.graph_params['k'].text(),
            'H': tab.graph_params['H'].text(),
            'n': tab.graph_params['n'].text(),
            'delta': tab.graph_params['delta'].text()
        }
        if ok:
            params['x_vals'] = self.point_manager.x
            params['y_vals'] = self.point_manager.y
        elif x_text or y_text:
            QMessageBox.warning(self.view, "Ошибка", msg)
            return
        graph_type = tab.graph_type.currentText()
        
        result = self.models['graph'].plot_graph(params, graph_type)

        if 'error' in result:
            QMessageBox.warning(self.view, "Ошибка", result['error'])
        else:
            tab.ax.clear()
            tab.ax.plot(result['x'], result['y'], color="blue")
            if result.get('points'):
                tab.ax.scatter(result['x'], result['y'], color="red", zorder=3)
            tab.ax.set_xlabel(result['xlabel'])
            tab.ax.set_ylabel(result['ylabel'])
            tab.ax.set_title(result['title'])
            if result['invert_y']:
                tab.ax.invert_yaxis()
            tab.canvas.draw()

    def load_points(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.view, "Открыть файл с точками", "", "Text/CSV Files (*.txt *.csv)"
        )
        if not file_path:
            return
        ok, msg = self.point_manager.load_from_file(file_path)
        if not ok:
            QMessageBox.warning(self.view, "Ошибка", msg)
            return
        tab = self.view.tabs["graphs"]
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