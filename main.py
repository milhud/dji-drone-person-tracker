import cv2
import numpy as np
import time
import math
import subprocess

auto_mode = False

# class for each person we detect
class Person:
    def __init__(self, person_id, location, color):
        # we give each person an id, where they are, and a color
        self.id = person_id
        self.cur_location = location  # where the person is right now
        self.trajectory = [location]  # track where they've been
        self.state = []  
        self.flag = 0  # flag to know if they've entered or left
        self.color = color  # color used to draw the person in the video

    def update_location(self, location):
        # we change where the person is, adding location to trajectory
        self.cur_location = location
        self.trajectory.append(location)

# class to keep track of all the people in the scene
class Tracker:
    def __init__(self, append_thresh=80):
        self.people = []  # storing people objects
        self.person_id = 0  # person id starts at 0  
        self.append_thresh = append_thresh  # how close they need to be to another person to be considered the same person
        # a list of colors so we can color people differently
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    def create_person(self, coord):
        # create a new person with an id and color
        color = self.colors[self.person_id % len(self.colors)]
        person = Person(self.person_id, coord, color)
        self.people.append(person)  # add the person to the list
        self.person_id += 1  # next person gets a new id

    def calculate_distance(self, a, b):
        # calculate distance between two points
        return np.linalg.norm(np.array(a) - np.array(b))

    def handle_tracker(self, cur_coords):
        for person in self.people: # loop throuhg people being tracked
            if cur_coords:
                distances = [self.calculate_distance(person.cur_location, coord) for coord in cur_coords] # calculates distance for each person
                min_index = np.argmin(distances) # index of closest person to detected coordinates
                min_dist = distances[min_index] 
                if min_dist < self.append_thresh: # if distance less than threshold, update location
                    person.update_location(cur_coords.pop(min_index))
        # create new person for any remaining coordinates
        for coord in cur_coords:
            self.create_person(coord)

def plot_trajectories(frame, people):
    for person in people: # loop through each perso and tracjetories
        prev_point = None
        for point in person.trajectory[:5]:
            x, y = point
            frame = cv2.circle(frame, (x, y), 3, person.color, cv2.FILLED) # draw circle at each point on tracjetory
            if prev_point is not None:
                frame = cv2.line(frame, prev_point, (x, y), person.color, 1) # line from previous  point to current one
            prev_point = (x, y)
    return frame

def run_tello_command(command):
    # sends commands to the Tello C++ program
    try:
        # subprocess for drone control program
        process = subprocess.Popen(
            ["./drone_control"],  # path to compiled c++ program
            stdin=subprocess.PIPE,  # pipe to send commands
            stdout=subprocess.PIPE,  # pip to read outputs
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send command
        process.stdin.write(command + "\n")
        process.stdin.flush()  # ensure command is sent
        process.wait()  # wait to finsih 
        
    except Exception as e: # in case of exception
        print(f"Error running Tello command: {e}")



def process_frame(frame, net, tracker, font):
    # does object detecting using yolo
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())

    class_ids, confidences, boxes = [], [], []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # 'person' class
                center_x, center_y, w, h = (detection[0:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])).astype(int)
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                boxes.append([x, y, w, h])
                class_ids.append(class_id)
                confidences.append(float(confidence))

    # Non-Maximum Suppression to eliminate overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    cur_coords = []
    
    # check if there are any detected people
    if len(indices) > 0: # prevent errors
        indices = indices.flatten()
        for i in indices:
            box = boxes[i]
            cur_coords.append([box[0] + int(box[2] / 2), box[1] + int(box[3] / 2)])
            cv2.rectangle(frame, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 2)

            x, y, w, h = box  # x, y, width, height of bounding box

            #estimate distance
            distance = estimate_distance(h)

            # draw box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # display distance on screen
            if distance:
                cv2.putText(frame, f"Dist: {distance:.2f}m", (x, y - 10), font, 1, (0, 255, 255), 2)

        # update tracker with current coordinates
        tracker.handle_tracker(cur_coords)

        # plot trajectories of people
        frame = plot_trajectories(frame, tracker.people)

        # display peopel count
        cv2.putText(frame, f"People Count: {len(tracker.people)}", (550, 30), font, 1.5, (255, 87, 221), 2)

        #if auto_mode is enabled, move towards the person
        if auto_mode and len(tracker.people) > 0:
            person = tracker.people[-1]  # get recent person detected
            person_coord = person.cur_location
            frame_width, frame_height = frame.shape[1], frame.shape[0]

            # calculate distance to center of the frame
            distance_to_center = calculate_distance_to_center(person_coord, frame_width, frame_height)

            # get coordinates
            x, y = person_coord
            center_x, center_y = frame_width / 2, frame_height / 2

            # move towards the center
            if x < center_x - 50:  #to left
                run_tello_command("turn_left")
            elif x > center_x + 50:  # to right
                run_tello_command("turn_right")
            elif y < center_y - 50:  # above
                run_tello_command("move_up")
            elif y > center_y + 50:  # below
                run_tello_command("move_down")

            # if distance is increasing, move forward
            if distance_to_center > 100:  # threshold for moving forward
                run_tello_command("move_forward")
            elif distance_to_center < 50:  # threshold for moving backwards
                run_tello_command("move_back")

    return frame

def estimate_distance(box_height, known_height=1.7, focal_length=800):
    # using camera focal length, box height in pixels, and known height of average person
    if box_height > 0:
        return (known_height * focal_length) / (box_height * 10) # estimated distance in meters
    return None

def calculate_distance_to_center(coord, frame_width, frame_height):
    # uses distance of person, x and y coordinates, and frame coords to determine distance to cetner
    center_x, center_y = frame_width / 2, frame_height / 2
    return np.linalg.norm(np.array(coord) - np.array([center_x, center_y]))

def track_person_and_move(frame, tracker):
    if tracker.people:
        person = tracker.people[-1]  # tracking most recent person
        person_coord = person.cur_location
        
        frame_width, frame_height = frame.shape[1], frame.shape[0]

        # distance from person to the center
        distance_to_center = calculate_distance_to_center(person_coord, frame_width, frame_height)
        
        # analyze relative position and decide on movement
        center_x, center_y = frame_width / 2, frame_height / 2
        x, y = person_coord
        
        # move towards center (if person is to the left or right, or up/down)
        if x < center_x - 50:  # if left
            run_tello_command("turn_left")  
        elif x > center_x + 50:  # if right
            run_tello_command("turn_right")  
        elif y < center_y - 50:  # if  above
            run_tello_command("move_up")  
        elif y > center_y + 50:  # if below
            run_tello_command("move_down") 

        # If the distance is growing (moving farther away), move forward
        if distance_to_center > 100:  # 
            run_tello_command("move_forward") 
        elif distance_to_center < 50:  # if too close to the center, maybe move backward
            run_tello_command("move_back")  # Move back

def main():
    video_source = 0 # must change depending on video source for DJI drone
    cap = cv2.VideoCapture(video_source)
    net = cv2.dnn.readNet("yolov3/yolov3.weights", "yolov3/yolov3.cfg")
    classes = open("yolov3/coco.names").read().strip().split('\n')

    tracker = Tracker()
    font = cv2.FONT_HERSHEY_TRIPLEX
    is_processing_enabled = True  # to avoid coflict, renamed flag

    while True:
        start_time = time.time()
        ret, frame = cap.read()
        
        if not ret or frame is None:  # check if frame is valid
            print("Exiting loop - no captured frame")
            break  # Exit the loop if no frame is captured
        
        frame = cv2.resize(frame, (1000, 750))

        if is_processing_enabled:
            frame = process_frame(frame, net, tracker, font=font)

        cv2.putText(frame, f"FPS: {1 / (time.time() - start_time):.2f}", (10, 30), font, 1.5, (0, 0, 255), 2)
        
        # check if frame is not none, then shows person tracking
        if not frame is None: 
            cv2.imshow("Person Tracking", frame)

        # keybindings to control drone program
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):
            is_processing_enabled = not is_processing_enabled
        if not is_processing_enabled:
            tracker.people.clear()
        elif key == ord('w') or key == 82:  # Move forward
            print("Move Forward")
            run_tello_command("move_forward")
        elif key == ord('s') or key == 84:  # backward
            print("Move Backward")
            run_tello_command("move_back")
        elif key == ord('a') or key == 81:  # left 
            print("Move Left")
            run_tello_command("move_left")
        elif key == ord('d') or key == 83:  # right 
            print("Move Right")
            run_tello_command("move_right")
        elif key == ord('r'):  #  up
            print("Move Up")
            run_tello_command("move_up")
        elif key == ord('f'):  # down
            print("Move Down")
            run_tello_command("move_down")
        elif key == ord('j'):  # rotate left
            print("Rotate Left")
            run_tello_command("turn_left")
        elif key == ord('l'):  # Rotate right
            print("Rotate Right")
            run_tello_command("turn_right")
        elif key == ord('k'):  # Stop movement, land
            print("Stop")
            run_tello_command("land")
        elif key == ord('m'): # turn auto mode on
            print("turning automode on")
            auto_mode = True
    
    return True

    # close program
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
