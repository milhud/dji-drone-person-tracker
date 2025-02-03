# DJI Drone Tracker & Follower

This repository contains the necessary code to detect and follow people using a DJI drone (with supported firmware).

Requirements:
- MonaServer (for RTMP streaming support)
- OBS Studio (for receiving RTMP broadcast) v31.0.0 
- DJI drone (Ryze Tello line)
- Python3
- C++ 14 (or higher) 
- CMake (for compiling drone_control for yourself)

(Implements [HerrNamenlos123's C++ library for communicating via the Tello SDK 2.0 library, in accordance with his license]).)

## To use:

First, clone this repository:

```.
git clone https://github.com/milhud/dji-drone-person-tracker.git
```
then download "tello.hpp" from [here](https://github.com/HerrNamenlos123/tello) and include it in the project directory.

Ensure the OpenCV library is installed for Python:

```.
pip install opencv
```

Then, install MonaServer at [this link](https://github.com/MonaSolutions/MonaServer), and OBS [here](https://obsproject.com/download).

After that is set up, create an RTMP broadcast from the Tello app (click the three dots -> create broadcast). Add a remote video stream on OBS, entering this URL, and then add this video source as a virtual camera.

Because the yolov3.weights file was too large, you must download it [here](https://github.com/patrick013/Object-Detection---Yolov3/blob/master/model/yolov3.weights) and add it to the yolov3 directory.

Then, with the OBS window open, you can run the Python program from the directory with:

```.
python main.py
```

which will use YOLOv3 to identify people and follow them automatically (should you activate auto mode). Edit the 'video_source' variable in main.py to switch it to the virtual camera in OBS.  

To control the program and activate automode, use the following keybindings:

| Key Pressed       | Action                      | Command Sent to Drone  |
|-------------------|-----------------------------|------------------------|
| `q`               | Quit the program            | ---                    |
| `p`               | Toggle processing on/off    | ---                    |
| `w`               | Move forward                | `move_forward`         |
| `s`               | Move backward               | `move_back`            |
| `a`               | Move left                   | `move_left`            |
| `d`               | Move right                  | `move_right`           |
| `r`               | Move up                     | `move_up`              |
| `f`               | Move down                   | `move_down`            |
| `j`               | Rotate left                 | `turn_left`            |
| `l`               | Rotate right                | `turn_right`           |
| `k`               | Stop movement, land         | `land`                 |
| `m`               | Enable auto mode            | `auto_mode = True`     |



Note: you can use the program without the drone attachment by running main.py

### Example:

To compile drone_control.exe for yourself, use the following commands in terminal:

```
cd example
mkdir build
cd build
cmake ..
cmake --build .
```

This will compile drone_control.exe and place it in the Debug folder.
