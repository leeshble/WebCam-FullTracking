import cv2
import cmath as np
import mediapipe as mp
from pythonosc import udp_client

# Set OSC client
client = udp_client.SimpleUDPClient('127.0.0.1', 39570)

scaler = 1.  # Scale value
height = 0.  # y-axis translation
waistS = 50.

# Array witch stored information of each body parts(mediapipe landmarks numbers and tracker information)
# (array index, body parts index, "device name", "device index(name within VMT)", landmark number for calculate angle(Two value))
body_parts_array = [
    (0, mp.solutions.pose.PoseLandmark.LEFT_WRIST, "LHR-leftHand", "Character1_LeftHand", (15, 17)),
    (1, mp.solutions.pose.PoseLandmark.RIGHT_WRIST, "LHR-rightHand", "Character1_RightHand", (16, 18)),
    (2, mp.solutions.pose.PoseLandmark.LEFT_ELBOW, "LHR-leftElbow", "Character1_LeftForeArm", (13, 15)),
    (3, mp.solutions.pose.PoseLandmark.RIGHT_ELBOW, "LHR-rightElbow", "Character1_RightForeArm", (14, 16)),
    (4, mp.solutions.pose.PoseLandmark.LEFT_KNEE, "LHR-leftKnee", "Character1_LeftLeg", (25, 27)),
    (5, mp.solutions.pose.PoseLandmark.RIGHT_KNEE, "LHR-rightKnee", "Character1_RightLeg", (26, 28)),
    (6, mp.solutions.pose.PoseLandmark.LEFT_ANKLE, "LHR-leftFoot", 11, (27, 29)),
    (7, mp.solutions.pose.PoseLandmark.RIGHT_ANKLE, "LHR-rightFoot", 12, (28, 30)),
    (8, mp.solutions.pose.PoseLandmark.LEFT_HIP, "LHR-leftHip", "Character1_LeftUpLeg", (23, 25)),
    (9, mp.solutions.pose.PoseLandmark.RIGHT_HIP, "LHR-rightHip", "Character1_RightUpLeg", (24, 26)),
    (10, mp.solutions.pose.PoseLandmark.LEFT_SHOULDER, "LHR-leftShoulder", "Character1_LeftShoulder", (11, 13)),
    (11, mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER, "LHR-rightShoulder", "Character1_RightShoulder", (12, 14))
]


# Poss detector class
class PoseDetector:

    def __init__(self, mode=False, complexity=1, smooth=True, detection=0.5, tracking=0.5, results=[]):
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.detection = detection
        self.tracking = tracking

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.detection, self.tracking)
        self.results = results

    # Save pose position value and draw landmark on frame
    def set_pose_data(self, frame, draw=True):
        # Array that to store tracker data
        tracker_data = []

        # Change the color of the frame for pose estimation
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # save results
        self.results = self.pose.process(frame_rgb)

        # Prevent error when self.results.pose_world
        try:
            # If self.results.pose_world_landmarks is available
            if self.results.pose_world_landmarks:
                landmarks = self.results.pose_world_landmarks.landmark

                # Draw landmarks on frame
                if draw:
                    self.mpDraw.draw_landmarks(frame, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

                # Set pose data to tracker data
                tracker_data.append(set_tracker_data1(landmarks))
                tracker_data.append(set_tracker_data2(landmarks))

        # Pass when exception occurred
        except:
            pass

        # self.results.pose_world is null, than pass
        return frame


# Set tracker data without waist
def set_tracker_data1(landmarks):
    tracker_data = []
    for index, part_name, serial, body_part, NBindex in body_parts_array:
        # Get angle from landmarks
        angle = calc_angle(landmarks[NBindex[0]], landmarks[NBindex[1]])

        # get x,y,z position data
        x = landmarks[part_name].x
        y = landmarks[part_name].y
        z = landmarks[part_name].z

        # Append tracker data with transform data
        tracker_data.append([body_part, x * scaler, y * scaler * (-1.) + height, z * scaler, angle[0],
                             angle[1], angle[2], 0., serial])

        # Send osc msg to openvr driver(VMT)
        send_osc_msg1(tracker_data[index][0], tracker_data[index][1], tracker_data[index][2], tracker_data[index][3],
                      tracker_data[index][4], tracker_data[index][5], tracker_data[index][6], tracker_data[index][7])


# Set waist data to tracker data
def set_tracker_data2(landmarks):
    tracker_data = []
    # Get Left_hip과 right_hip의 중간 좌표 계산(원점)
    left_hip = landmarks[23]
    right_hip = landmarks[24]
    mid_hip = mid_point(left_hip, right_hip)

    # Quaternion x, y, z, w value is example. IT MUST FIXED WITH ADDITIONAL CALCULATION
    # The waist part requires a separate calculation, so it is independent
    # tracker_data.append([10, mid_hip[0] * scaler * waistS, mid_hip[1] * scaler * waistS + height,
    #                     mid_hip[2] * scaler * waistS, 0., 0., 0., 0., "waist"])
    tracker_data.append([10, 0., 0., 0., 0., 0., 0., 0., 0., "waist"])

    # Send osc msg to openvr driver(VMT)
    send_osc_msg1(tracker_data[0][0], tracker_data[0][1], tracker_data[0][2], tracker_data[0][3], tracker_data[0][4],
                  tracker_data[0][5], tracker_data[0][6], tracker_data[0][7])
    return tracker_data


# Convert roll, pitch, yaw into quaternion
def conv_quat(roll, pitch, yaw):
    qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
    qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
    qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
    qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
    return qx, qy, qz, qw


# Input position of two dots and retrieve position of mid point(to get position of waist)
def mid_point(pos_1, pos_2):
    mid_pos_x = (pos_1.x + pos_2.x) / 2
    mid_pos_y = (pos_1.y + pos_2.y) / 2
    mid_pos_z = (pos_1.z + pos_2.z) / 2
    mid_pos = (mid_pos_x, mid_pos_y, mid_pos_z)
    return mid_pos


# calculate angle with two landmarks points
def calc_angle(point1, point2):
    x = point2.x - point1.x
    y = point2.y - point1.y
    z = point2.z - point1.z
    return x, y, z


# Send osc msg to openvr driver(VMT)
# (device index, position x, position y, position z, quaternion x, quaternion y, quaternion z, quaternion w)
def send_osc_msg1(index, px, py, pz, qx, qy, qz, qw):
    client.send_message("/VMT/Room/Unity", [index, 1, 0., px, py, pz, qx, qy, qz, qw])


# Send osc msg to openvr driver(VMT)
# (device index, position x, position y, position z, quaternion x, quaternion y, quaternion z, quaternion w, HMD serial)
def send_osc_msg2(index, px, py, pz, qx, qy, qz, qw, serial):
    client.send_message("/VMT/Joint/Unity", [index, 1, 0., px, py, pz, qx, qy, qz, qw, serial])
