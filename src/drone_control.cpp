#include <iostream>
#include "../tello/tello.hpp"  // include header file for library to communicate with drone
#include <string>
#include <thread>
#include <atomic>

class DroneController {
private:
    Tello tello;  // instantiate Tello object

public:
    DroneController() {
        if (!tello.connect()) {
            std::cerr << "Failed to connect to Tello." << std::endl;
            exit(1);  // exit if connection fails
        }
    }

    ~DroneController() {
        tello.land();  // destructor to ensure the drone lands safely when the program ends
    }

    void takeOff() {
        tello.takeoff();
        std::cout << "Drone taking off." << std::endl;
    }

    void land() {
        tello.land();
        std::cout << "Drone landing." << std::endl;
    }

    void moveUp() {
        tello.move_up(20);  // move up by 20 cm
        std::cout << "Drone moving up." << std::endl;
    }

    void moveDown() {
        tello.move_down(20);  // down by 20 cm
        std::cout << "Drone moving down." << std::endl;
    }

    void moveLeft() {
        tello.move_left(20);  // left by 20 cm
        std::cout << "Drone moving left." << std::endl;
    }

    void moveRight() {
        tello.move_right(20);  // right by 20 cm
        std::cout << "Drone moving right." << std::endl;
    }

    void moveForward() {
        tello.move_forward(30);  // forward by 30 cm
        std::cout << "Drone moving forward." << std::endl;
    }

    void moveBack() {
        tello.move_back(30);  // backwards by 30 cm
        std::cout << "Drone moving back." << std::endl;
    }

    void turnLeft() {
        tello.turn_left(45);  // Turn left by 90 degrees
        std::cout << "Drone turning left." << std::endl;
    }

    void turnRight() {
        tello.turn_right(45);  // right by 45 degrees
        std::cout << "Drone turning right." << std::endl;
    }

    // receives and executes commands
    void executeCommand(const std::string& command) {
        if (command == "move_up") {
            moveUp();
        } else if (command == "move_down") {
            moveDown();
        } else if (command == "move_left") {
            moveLeft();
        } else if (command == "move_right") {
            moveRight();
        } else if (command == "move_forward") {
            moveForward();
        } else if (command == "move_back") {
            moveBack();
        } else if (command == "turn_left") {
            turnLeft();
        } else if (command == "turn_right") {
            turnRight();
        } else if (command == "land") {
            land();
        } else {
            std::cerr << "Invalid command!" << std::endl;
        }
    }
};

// listens for commands
void listenForCommands(DroneController &drone) {
    std::string command;
    while (true) {
        std::getline(std::cin, command);  // Read command from stdin
        if (command == "exit") {
            break;  // exit the loop when 'exit' command is received
        }
        drone.executeCommand(command);  // execute the command
    }
}

int main() {
    DroneController drone;

    drone.takeOff();  // drone begins by taking off

    std::thread listener(listenForCommands, std::ref(drone));  // Start the listener in a separate thread

    listener.join();  // listesn for "exit" - waits to finish

    drone.land();  // ensure  drone lands upon exit
    return 0;
}