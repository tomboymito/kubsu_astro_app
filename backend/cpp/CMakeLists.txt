cmake_minimum_required(VERSION 3.15)
project(comet_calculations VERSION 1.0.0)

# 1. Явное добавление подмодуля pybind11 вместо find_package
add_subdirectory(pybind11)

# Настройка Python
set(Python3_EXECUTABLE "C:/Program Files/Python311/python.exe")
find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter Development)

# 2. Удален find_package для pybind11, так как используем add_subdirectory
# Проверка исходных файлов
set(SOURCES
    core/sublimation.cpp
    core/mass.cpp
    core/nucleus.cpp
)

foreach(src ${SOURCES})
    if(NOT EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${src})
        message(FATAL_ERROR "Missing source file: ${src}")
    endif()
endforeach()

# Создание модуля Python
pybind11_add_module(comet_calculations ${SOURCES})

# Настройка включаемых директорий
target_include_directories(comet_calculations PRIVATE
    ${PROJECT_SOURCE_DIR}/include
    ${Python3_INCLUDE_DIRS}
)

# 3. Исправлена опечатка в PROPERTIES (было PROPERTIES)
# Настройка выходного каталога
# В файле backend/cpp/CMakeLists.txt измените:
set(OUTPUT_DIR "${CMAKE_SOURCE_DIR}/backend/app/core/calculations")
file(MAKE_DIRECTORY ${OUTPUT_DIR})

# Платформо-зависимые настройки
if(WIN32)
    set_target_properties(comet_calculations PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_DIR}
        SUFFIX ".pyd"
        PREFIX ""
    )
else()
    set_target_properties(comet_calculations PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_DIR}
        SUFFIX ".so"
    )
endif()

# 4. Добавлена явная линковка с Python
target_link_libraries(comet_calculations PRIVATE
    ${Python3_LIBRARIES}
)

message(STATUS "Comet calculations module will be built in: ${OUTPUT_DIR}")