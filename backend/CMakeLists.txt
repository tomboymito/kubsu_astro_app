cmake_minimum_required(VERSION 3.12)
project(comet_backend)

# Настройка pybind11
find_package(Python REQUIRED COMPONENTS Development)
find_package(pybind11 REQUIRED)

# Модуль для расчетов сублимации
add_subdirectory(cpp)