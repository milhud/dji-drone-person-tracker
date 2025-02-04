#include <iostream>
#include "../tello/tello.hpp"

int main() {
    Tello tello;

    // Connect to the drone
    if (!tello.connect()) {
        std::cerr << "Failed to connect to Tello drone." << std::endl;
        return 1;
    }

    // Activate the camera stream
    if (!tello.enable_video_stream()) {
        std::cerr << "Failed to enable video stream." << std::endl;
        return 1;
    }

    std::cout << "Video stream activated." << std::endl;

    return 0;
}