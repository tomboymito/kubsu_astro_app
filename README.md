# **| Создание .exe и запуск приложения |**

### *при создании .exe следует отредактировать файл 'app/main.py'*
```app/main.py
import sys
from PyQt5.QtWidgets import QApplication
from app.views import MainWindow
from app.controllers import MainController
from app.models import SublimationModel, GraphModel, MassModel, SizeModel
```

## 1. Уставноить requirements.txt
```
pip install -r requirements.txt
```

## 2. Скачать PyInstaller
```
pip install PyInstaller
```

## 3. Создать файл .exe
```
python -m PyInstaller KUBSU_Astro_App.spec
```

# **| Запуск приложения для теста |**

### *при запуске приложения для теста следует отредактировать файл 'app/main.py'*
```app/main.py
import sys
from PyQt5.QtWidgets import QApplication
from views import MainWindow
from controllers import MainController
from models import SublimationModel, GraphModel, MassModel, SizeModel
```

## 1. Уставноить requirements.txt
```
pip install -r requirements.txt
```

## 2. Запустить 'app/main.py'
```
python app/main.py
```
После нажатия кнопки «Построить график» результат откроется в отдельном окне.
В нём можно увидеть координаты текущего положения курсора в правом верхнем углу,
на графике включена сетка.
## Пример файла с точками
Для проверки загрузки собственных данных можно использовать файл `data/sample_points.csv`. Он содержит две колонки (X и Y), разделённые запятой. В окне приложения выберите "Загрузить точки из файла" на вкладке «Графики» и укажите этот файл.
