cmake_minimum_required(VERSION 3.12)
project(comet_calculations)

# Настройка Python и pybind11
find_package(Python 3.12 REQUIRED COMPONENTS Development)
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 REQUIRED)

# Добавляем модуль
pybind11_add_module(comet_calculations
    core/sublimation.cpp
    core/mass.cpp
    core/nucleus.cpp
)

# Указываем включаемые директории
target_include_directories(comet_calculations PRIVATE
    ${PROJECT_SOURCE_DIR}/include
)

# Для macOS специфические настройки
if(APPLE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -stdlib=libc++")
endif()

# Устанавливаем выходной каталог
set_target_properties(comet_calculations PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/../app/core/calculations
    SUFFIX ".so"
)