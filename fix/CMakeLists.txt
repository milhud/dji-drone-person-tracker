cmake_minimum_required(VERSION 3.10)
project(TelloCamera)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the executable
add_executable(tello_camera_fix fix_camera.cpp)

if(WIN32)
    target_link_libraries(tello_camera_fix ws2_32)
endif()