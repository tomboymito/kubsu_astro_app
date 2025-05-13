cmake_minimum_required(VERSION 3.15)
project(comet_calculations)

# Явно указываем путь к Python
set(Python3_ROOT_DIR "C:/Program Files/Python311")
find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter Development)

# Вариант 1: Если pybind11 установлен через pip
# find_package(pybind11 REQUIRED)
# Или укажите явный путь, если CMake не находит
# set(pybind11_DIR "C:/path/to/pybind11/share/cmake/pybind11")

# Вариант 2: Если используете pybind11 как подмодуль
add_subdirectory(pybind11)

# Проверка исходных файлов
foreach(src core/sublimation.cpp core/mass.cpp core/nucleus.cpp)
    if(NOT EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${src})
        message(FATAL_ERROR "Missing source file: ${src}")
    endif()
endforeach()

# Создаём модуль
pybind11_add_module(comet_calculations
    core/sublimation.cpp
    core/mass.cpp
    core/nucleus.cpp
)

# Настройки включаемых директорий
target_include_directories(comet_calculations PRIVATE
    ${PROJECT_SOURCE_DIR}/include
    ${Python3_INCLUDE_DIRS}
)

# Настройки выходного каталога
set(OUTPUT_DIR ${PROJECT_SOURCE_DIR}/../app/core/calculations)
file(MAKE_DIRECTORY ${OUTPUT_DIR})

if(WIN32)
    set_target_properties(comet_calculations PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_DIR}
        SUFFIX ".pyd"
        PREFIX ""  # Убираем 'lib' в начале имени
    )
else()
    set_target_properties(comet_calculations PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_DIR}
        SUFFIX ".so"
    )
endif()