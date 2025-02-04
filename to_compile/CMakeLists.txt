cmake_minimum_required(VERSION 3.0.2)
project(drone_control LANGUAGES CXX)

add_library(tello INTERFACE)

target_include_directories(tello INTERFACE ${CMAKE_SOURCE_DIR}/../tello)

set(SOURCES
    src/drone_control.cpp
)

# Create the executable target 
add_executable(drone_control ${SOURCES})

target_link_libraries(drone_control tello)
target_include_directories(drone_control PUBLIC 
    ${CMAKE_SOURCE_DIR}/../tello  # Include tello.hpp
    ${CMAKE_SOURCE_DIR}/src       # Include source files
)

if (NOT MSVC)
    target_link_libraries(drone_control pthread)
endif()

# Compiler options for C++14
if (MSVC)
    target_compile_options(drone_control PUBLIC /std:c++14)
else()
    target_compile_options(drone_control PUBLIC -std=c++14)
endif()
