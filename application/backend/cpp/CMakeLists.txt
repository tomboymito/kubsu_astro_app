cmake_minimum_required(VERSION 3.15)
project(comet_calculations VERSION 1.0.0)

# Правильный путь к папке назначения (теперь внутри backend)
set(OUTPUT_DIR "${CMAKE_SOURCE_DIR}/../app/core/calculations")
file(MAKE_DIRECTORY ${OUTPUT_DIR})

# Настройка вывода для Visual Studio
if(MSVC)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${OUTPUT_DIR})
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${OUTPUT_DIR})
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_DIR})
    set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${OUTPUT_DIR})
endif()

add_subdirectory(pybind11)
find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter Development)

set(SOURCES
    core/sublimation.cpp
    core/mass.cpp
    core/nucleus.cpp
)

pybind11_add_module(comet_calculations ${SOURCES})

target_include_directories(comet_calculations PRIVATE
    ${PROJECT_SOURCE_DIR}/include
    ${Python3_INCLUDE_DIRS}
)

if(WIN32)
    set_target_properties(comet_calculations PROPERTIES
        SUFFIX ".pyd"
        PREFIX ""
    )
endif()

target_link_libraries(comet_calculations PRIVATE ${Python3_LIBRARIES})

message(STATUS "Output will be directed to: ${OUTPUT_DIR}")