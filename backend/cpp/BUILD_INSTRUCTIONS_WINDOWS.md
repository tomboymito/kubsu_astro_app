# Инструкция по сборке C++ библиотек для проекта kubsu_astro_app на Windows

## Требования

- Установленный CMake (https://cmake.org/download/)
- Установленный компилятор C++ (например, Microsoft Visual Studio с компонентом "Desktop development with C++")
- Python 3.10 (уже установлен, судя по проекту)
- Активированное виртуальное окружение Python (venv)

## Шаги сборки

1. Откройте PowerShell или командную строку (cmd).

2. Перейдите в директорию с исходниками C++:
   ```
   cd path\to\kubsu_astro_app\backend\cpp
   ```
   Например:
   ```
   cd C:\Users\maxvl\repos\kubsu_astro_app\backend\cpp
   ```

3. Создайте папку для сборки и перейдите в неё:
   ```
   mkdir build
   cd build
   ```

4. Запустите конфигурацию CMake:
   ```
   cmake .. -DCMAKE_BUILD_TYPE=Release
   ```
   Эта команда подготовит файлы сборки для вашей системы.

5. Запустите сборку проекта:
   ```
   cmake --build . --config Release
   ```
   Эта команда скомпилирует C++ код и создаст файл `comet_calculations.pyd`.

6. После успешной сборки файл `comet_calculations.pyd` появится в директории:
   ```
   backend\app\core\calculations\
   ```

7. Теперь вы можете запустить FastAPI сервер:
   ```
   backend\venv\Scripts\uvicorn.exe backend.main:app --host 0.0.0.0 --port 8000
   ```

## Возможные проблемы

- Если CMake не найден, убедитесь, что он добавлен в PATH.
- Если компилятор не найден, установите Visual Studio с компонентом C++.
- Если возникают ошибки сборки, пожалуйста, предоставьте логи для анализа.