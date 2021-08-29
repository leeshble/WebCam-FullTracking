import cv2
import time
import mediapipe as mp
import math_module as mm
import osc_module as osc

pose = mp.solutions.pose.Pose(False, 1, True, 0.5, 0.5)
POSE_LANDMARK = [
    (0, "MPT-Head", (0, 7)),
    (11, "MPT-leftShoulder", (11, 13)),
    (12, "MPT-rightShoulder", (12, 14)),
    (13, "MPT-leftElbow", (15, 17)),
    (14, "MPT-rightElbow", (16, 18)),
    (15, "MPT-leftHand", (13, 15)),
    (16, "MPT-rightHand", (14, 16)),
    (23, "MPT-leftHip", (23, 25)),
    (24, "MPT-rightHip", (24, 26)),
    (25, "MPT-leftKnee", (25, 27)),
    (26, "MPT-rightKnee", (26, 28)),
    (27, "MPT-leftFoot", (27, 26)),
    (28, "MPT-rightFoot", (28, 30))
]


def camera_input(input_data):
    p_time = 0
    cap = cv2.VideoCapture(input_data)
    while True:
        success, frame = cap.read()
        if success:
            landmarks = pose_detection(frame)
            if landmarks is not None:
                conv_data_openvr(get_position_data(landmarks))
        fps, p_time = fps_count(p_time)
        print("FPS: %d" % fps)
        cv2.imshow("Capture", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    print()
    cap.release()
    cap.destroyAllWindows()


def pose_detection(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)
    try:
        landmarks = results.pose_world_landmarks.landmark
        return landmarks
    except:
        pass


def get_position_data(landmarks):
    position_data = []
    for i in range(0, 32):
        position_data.append([i, landmarks[i].x, landmarks[i].y, landmarks[i].z])
    return position_data

"""
def conv_data_openvr(position_data):
    device_data = []
    for index, device_name, comp_pos in POSE_LANDMARK:
        u = mm.Vector(position_data[comp_pos[0]][1], position_data[comp_pos[0]][2], position_data[comp_pos[0]][3])
        v = mm.Vector(position_data[comp_pos[1]][1], position_data[comp_pos[1]][2], position_data[comp_pos[1]][3])
        qx, qy, qz, qw = mm.landmarks2quaternion(u, v)
        device_data.append(
            [index, 1, 0., position_data[index][1], -position_data[index][2], position_data[index][3], qx, qy, qz, qw])
        osc.osc_send(index, 1, 0., position_data[index][1], -position_data[index][2], position_data[index][3], qx, qy, qz, qw)
    return device_data
"""


def conv_data_openvr(position_data):
    device_data = []
    for index, device_name, comp_pos in POSE_LANDMARK :
        u = mm.Vector(position_data[comp_pos[0]][1], position_data[comp_pos[0]][2], position_data[comp_pos[0]][3])
        v = mm.Vector(0, 0, 10)
        qx, qy, qz, qw = mm.landmarks2quaternion(u, v)
        device_data.append(
            [index, 1, 0., position_data[index][1], -position_data[index][2], position_data[index][3], qx, qy, qz, qw])
    # device_data.append([-1, 1, 0., (position_data[7][1] + position_data[8][1]) / 2, (position_data[7][2] + position_data[8][2]) / 2, (position_data[7][1] + position_data[8][1]) / 2])
        osc.osc_send(index, 1, 0., position_data[index][1], -position_data[index][2], position_data[index][3], qx, qy, qz, qw)
    return device_data


def fps_count(p_time):
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    # avg_fps = (avg_fps + c_time) / 2
    return int(fps), c_time
