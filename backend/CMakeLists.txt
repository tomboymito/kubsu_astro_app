cmake_minimum_required(VERSION 3.15)
project(comet_calculations)

set(CMAKE_CXX_STANDARD 17)

# Явно указываем Python (если CMake не находит автоматически)
set(Python3_ROOT_DIR "C:/Program Files/Python311")
find_package(Python3 3.11 EXACT REQUIRED COMPONENTS Interpreter Development)

# Добавляем pybind11 (либо через add_subdirectory, либо find_package)
add_subdirectory(cpp/pybind11)  # или find_package(pybind11 REQUIRED)

# Создаём модуль Python
pybind11_add_module(libcomet_calculations
    core/sublimation.cpp
    core/mass.cpp
    core/nucleus.cpp
)

# Подключаем зависимости
target_include_directories(libcomet_calculations PRIVATE ${Python3_INCLUDE_DIRS})
target_link_libraries(libcomet_calculations PRIVATE ${Python3_LIBRARIES} pybind11::module)