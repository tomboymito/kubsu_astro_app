import numpy as np

class PointManager:
    def __init__(self):
        self.x = np.array([])
        self.y = np.array([])

    def _parse_text(self, text: str):
        text = text.strip()
        if not text:
            return []
        if ',' in text and ' ' not in text:
            parts = text.split(',')
        else:
            parts = text.replace(',', ' ').split()
        return parts

    def validate_points(self, x_text: str, y_text: str):
        x_parts = self._parse_text(x_text)
        y_parts = self._parse_text(y_text)
        if not x_parts or not y_parts:
            return False, "Нужно задать списки X и Y"
        if len(x_parts) != len(y_parts):
            return False, "Количество точек X и Y должно совпадать"
        if len(x_parts) < 2:
            return False, "Необходимо минимум 2 точки"
        try:
            self.x = np.array([float(v) for v in x_parts])
            self.y = np.array([float(v) for v in y_parts])
        except ValueError:
            return False, "Точки должны быть числами"
        return True, ""

    def load_from_file(self, file_path: str):
        x_vals = []
        y_vals = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.replace(';', ',').replace(',', ' ').split()
                if len(parts) >= 2:
                    try:
                        x_vals.append(float(parts[0]))
                        y_vals.append(float(parts[1]))
                    except ValueError:
                        continue
        self.x = np.array(x_vals)
        self.y = np.array(y_vals)
        if len(self.x) < 2 or len(self.x) != len(self.y):
            return False, "Некорректные данные в файле"
        return True, ""

    def get_plot_data(self):
        return {'x': self.x, 'y': self.y}