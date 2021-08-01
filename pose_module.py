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
