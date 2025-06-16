import sys
from PyQt5.QtWidgets import QApplication
from app.views import MainWindow
from app.controllers import MainController
from app.models import SublimationModel, GraphModel, MassModel, SizeModel

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Создание моделей
    models = {
        'sublimation': SublimationModel(),
        'graph': GraphModel(),
        'mass': MassModel(),
        'size': SizeModel()
    }
    
    # Создание представления
    view = MainWindow()
    
    # Создание контроллера
    controller = MainController(models, view)
    
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()