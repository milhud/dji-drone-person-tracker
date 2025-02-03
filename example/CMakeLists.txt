cmake_minimum_required(VERSION 3.0.2)
project(example LANGUAGES CXX)

# Define the tello header-only library as an INTERFACE library
add_library(tello INTERFACE)

# Include the tello folder from the parent directory
target_include_directories(tello INTERFACE ${CMAKE_SOURCE_DIR}/../tello)

# Add source files for your executable (from example/src folder)
set(SOURCES
    src/drone_control.cpp
)

# Create the executable target
add_executable(example ${SOURCES})

# Link the tello INTERFACE library (ensures the header file is found)
target_link_libraries(example tello)

# Ensure the example target includes the tello headers and src directory
target_include_directories(example PUBLIC 
    ${CMAKE_SOURCE_DIR}/../tello  # Include tello.hpp
    ${CMAKE_SOURCE_DIR}/src       # Include example source files
    ${CMAKE_SOURCE_DIR}/include   # Include additional headers (optional)
)

# If not using MSVC (e.g., Linux), link pthread
if (NOT MSVC)
    target_link_libraries(example pthread)
endif()

# Compiler options for C++14
if (MSVC)
    target_compile_options(example PUBLIC /std:c++14)
else()
    target_compile_options(example PUBLIC -std=c++14)
endif()