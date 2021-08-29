"""
import cv2
import mediapipe as mp

# type in mm value
room_size_x = 1
room_size_y = 1
room_size_z = 1


# Calculate quaternion
def cal_quaternion(main_pos_x, main_pos_y, main_pos_z, sub_pos_x, sub_pos_y, sub_pos_z):
    quaternion_data = [[main_pos_x - sub_pos_x, main_pos_y - sub_pos_y, main_pos_z - sub_pos_z]]
    clean_pose_data(quaternion_data)

def clean_pose_data(pose_data, quaternion_data):
    pose_data[0, quaternion_data[0], quaternion_data[1], quaternion_data[2], 0]

class PoseDetector:
    def __init__(self, mode=False, complexity=1, smooth=True, detection=0.5, tracking=0.5):
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.detection = detection
        self.tracking = tracking

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.detection, self.tracking)

    def find_pose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_world_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img


    def find_position(self, img, draw=True):
        pose_data = []
        if self.results.pose_world_landmarks:
            for id, lm in enumerate(self.results.pose_world_landmarks.landmark):
                pose_data.append([id, lm.x, lm.y, lm.z])
            cal_quaternion()
        return pose_data
"""

import cv2
import numpy as np
import mediapipe as mp
from pythonosc import udp_client
import osc_module as om

# Set OSC client
client = udp_client.SimpleUDPClient('127.0.0.1', 39570)

scaler = 1.  # 크기 확대
height = 1.  # y축 평행이동
waistS = 50.

body_parts_array = np.array([
    (mp.solutions.pose.PoseLandmark.LEFT_WRIST, "leftHand", "Character1_LeftHand", (15, 17)),
    (mp.solutions.pose.PoseLandmark.RIGHT_WRIST, "rightHand", "Character1_RightHand", (16, 18)),
    (mp.solutions.pose.PoseLandmark.LEFT_ELBOW, "leftElbow", "Character1_LeftForeArm", (13, 15)),
    (mp.solutions.pose.PoseLandmark.RIGHT_ELBOW, "rightElbow", "Character1_RightForeArm", (14, 16)),
    (mp.solutions.pose.PoseLandmark.LEFT_KNEE, "leftKnee", "Character1_LeftLeg", (25, 27)),
    (mp.solutions.pose.PoseLandmark.RIGHT_KNEE, "rightKnee", "Character1_RightLeg", (26, 28)),
    (mp.solutions.pose.PoseLandmark.LEFT_ANKLE, "leftFoot", "Character1_LeftFoot", (27, 29)),
    (mp.solutions.pose.PoseLandmark.RIGHT_ANKLE, "rightFoot", "Character1_RightFoot", (28, 30)),
    (mp.solutions.pose.PoseLandmark.LEFT_HIP, "leftHip", "Character1_LeftUpLeg", (23, 25)),
    (mp.solutions.pose.PoseLandmark.RIGHT_HIP, "rightHip", "Character1_RightUpLeg", (24, 26)),
    (mp.solutions.pose.PoseLandmark.LEFT_SHOULDER, "leftShoulder", "Character1_LeftShoulder", (11, 13)),
    (mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER, "rightShoulder", "Character1_RightShoulder", (12, 14))
], dtype=object)


# 포즈 인식 클래스
class PoseDetector:

    def __init__(self, mode=False, complexity=1, smooth=True, detection=0.5, tracking=0.5):
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.detection = detection
        self.tracking = tracking

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.detection, self.tracking)

    # 포즈 좌표값 저장 및 프레임에 그리기
    def set_pose_data(self, frame, draw=True):
        tracker_data = np.array([])
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(frame_rgb)
        landmarks = np.array(self.results.pose_world_landmarks.landmark)
        if self.results.pose_world_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(frame, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            for part_name, box_name, body_part, NBindex in body_parts_array:
                # Get angle from landmarks
                angle = calc_angle(landmarks[NBindex[0]], landmarks[NBindex[1]])
                x = landmarks[part_name].x
                y = landmarks[part_name].y
                z = landmarks[part_name].z

                # Send tracker data to Driver
                send_osc_msg(body_part, x * scaler, y * scaler * (-1.) + height, z * scaler, angle[0], angle[1],
                             angle[2], 0., box_name)
            # Set pose data to tracker data
            tracker_data = np.append(tracker_data, set_tracker_data1(landmarks))
            tracker_data = np.append(tracker_data, set_tracker_data2(landmarks))
        return frame, tracker_data


def set_tracker_data1(landmarks):
    tracker_data = np.array([])
    for part_name, box_name, body_part, NBindex in body_parts_array:
        # Get angle from landmarks
        angle = calc_angle(landmarks[NBindex[0]], landmarks[NBindex[1]])
        x = landmarks[part_name].x
        y = landmarks[part_name].y
        z = landmarks[part_name].z
        tracker_data = np.append(tracker_data,
                                 [body_part, x * scaler, y * scaler * (-1.) + height, z * scaler, angle[0],
                                  angle[1], angle[2], 0., box_name])
        send_osc_msg(body_part, x * scaler, y * scaler * (-1.) + height, z * scaler, angle[0],
                                  angle[1], angle[2], 0., box_name)
        #print(tracker_data)


# Set head and shoulder data
def set_tracker_data2(landmarks):
    tracker_data = np.array([])
    # Left_hip과 right_hip의 중간 좌표 계산(원점)
    mid_hip = mid_point(landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP],
                        landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP])
    # 양 어깨의 중간 좌표 계산
    mid_shoulder = mid_point(landmarks[11], landmarks[12])
    nose = landmarks[mp.solutions.pose.PoseLandmark.NOSE]
    head_angle_x = mid_shoulder[0] - nose.x
    head_angle_y = mid_shoulder[1] - nose.y
    head_angle_z = mid_shoulder[2] - nose.z
    tracker_data = np.append(tracker_data,
                             ["Character1_Head", nose.x * scaler, nose.y * scaler * (-1) + height, nose.z * scaler,
                              head_angle_x, head_angle_y, head_angle_z, 0., "head"])
    # 허리부분은 별도의 계산이 필요하므로 독립
    tracker_data = np.append(tracker_data,
                             ["Character1_Hips", mid_hip[0] * scaler * waistS, mid_hip[1] * scaler * waistS + height,
                              mid_hip[2] * scaler * waistS, 0., 0., 0., 0., "waist"])
    # Send tracker to VMT
    for i in range(0, 1):
        send_osc_msg(tracker_data[i][0], tracker_data[i][1], tracker_data[i][2], tracker_data[i][3], tracker_data[i][4],
                     tracker_data[i][5], tracker_data[i][6], tracker_data[i][7], tracker_data[i][8])
    return tracker_data


# 롤, 피치, 요를 사원수로 변환한다.
def conv_quat(roll, pitch, yaw):
    qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
    qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
    qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
    qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
    return qx, qy, qz, qw


# 두 점의 좌표를 입력받아 중점의 좌표를 반환한다.(허리의 좌표를 구하는 데 사용)
def mid_point(pos_1, pos_2):
    mid_pos_x = (pos_1.x + pos_2.x) / 2
    mid_pos_y = (pos_1.y + pos_2.y) / 2
    mid_pos_z = (pos_1.z + pos_2.z) / 2
    mid_pos = (mid_pos_x, mid_pos_y, mid_pos_z)
    return mid_pos


def calc_angle(point1, point2):
    x = point1.x - point2.x
    y = point1.y - point2.y
    z = point1.z - point2.z
    return x, y, z


"""
px = position_x
py = position_y
pz = position_z
qx = quaternion_x
qy = quaternion_y
qz = quaternion_z
w = quaternion_w
"""


def send_osc_msg(body_part, px, py, pz, qx, qy, qz, qw, box_name):
    client.send_message("/VMT/Room/Unity", [body_part, px, py, pz, qx, qy, qz, qw, box_name])
