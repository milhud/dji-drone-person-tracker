# DJI Drone Tracker & Follower

This repository contains the necessary code to detect and follow people using a DJI drone (with supported firmware).

Requirements:
- OBS Studio (for receiving RTMP broadcast) v31.0.0 
- DJI drone (Ryze Tello line)
- Python3
- C++ 14 (or higher) 
- CMake (for compiling drone_control for yourself)

(Implements [HerrNamenlos123's C++ library for communicating via the Tello SDK 2.0 library, in accordance with his license](https://github.com/HerrNamenlos123/tello/blob/master/tello.hpp)).

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

Then on OBS, click +, go to Sources, select Media Source, uncheck local file and enter `udp://0.0.0.0:11111` as the input (or whatever IP you want it to be). Press OK. Then, press Tools -> Start Virtual Camera.

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

### To Compile For Yourself:

To compile drone_control.exe for yourself, use the following commands in terminal:

```
cd to_compile
mkdir build
cd build
cmake ..
cmake --build .
```

This will compile as drone_control and place it in the Debug folder. Move this to main repository folder.

# Fix

It works on my computer, but there has been difficulty reproducing it on another machine with the deprecated Tello app. Instead, you can activate the video stream with the header library tello.hpp. The files you need should be in fix/

Then, connect to the drone's Wifi. 

Restart your computer and run the following commands from terminal (in the /fix directory):

```
tello_camera_fix.exe
```

Then on OBS, click +, go to Sources, select Media Source, uncheck local file and enter `udp://0.0.0.0:11111` as the input (or whatever IP you want it to be). Press OK. Then, press Tools -> Start Virtual Camera.

This should start a virtual camera, and you can continue using the program outlined in the steps above.

tello_camera_fix.exe has been compiled for your convenience, but you can generate the build files and compile it yourself with the following commands (from main repository folder).

```
cd fix
mkdir build
cd build
cmake ..
cmake --build .
```

This will place tello_camera_fix.exe in the Debug folder.



