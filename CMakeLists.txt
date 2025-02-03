cmake_minimum_required(VERSION 3.0.2)
project(example LANGUAGES CXX)

# This example uses the library with the CMake INTERFACE library.
# Alternatively you can just copy and paste 'tello.hpp' into your include folder.
# In this case, omit the 'add_subdirectory' and 'target_link_libraries' below.

# Define the tello header-only library as an INTERFACE library
add_library(tello INTERFACE ${CMAKE_SOURCE_DIR}/tello)

# Set the include directory for the tello INTERFACE library
target_include_directories(tello INTERFACE ${CMAKE_SOURCE_DIR}./tello.hpp)

# Add source files for your executable
set(SOURCES
    src/drone_control.cpp
)

# Create the executable target
add_executable(example ${SOURCES})

# Link the tello INTERFACE library (no need for actual linking)
target_link_libraries(example tello)

# Include directories for your executable target
target_include_directories(example PUBLIC include)

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
