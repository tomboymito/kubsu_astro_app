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
## Примеры файлов с точками
В каталоге `data` находятся примеры наборов данных для всех типов графиков:

- `test_afrho_r.txt` — Afρ от расстояния
- `test_mag_r.txt` — звёздная величина от расстояния
- `test_afrho_date.txt` — Afρ от даты
- `test_mag_date.txt` — звёздная величина от даты

Каждый файл содержит две колонки (X и Y), разделённые пробелом. Чтобы загрузить данные, выберите «Загрузить точки из файла» на вкладке «Графики» и укажите подходящий файл.
