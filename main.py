import cv2
import time
import pose_module as pm
import osc_module as osc
while True:
    # 비디오 또는 웹캠 불러오기
    cap = cv2.VideoCapture('Examples/2.mp4')
    # 프레임 확인을 위한 변수
    pTime = 0
    isclosed = 0
    detector = pm.PoseDetector()
    while True:
        success, img = cap.read()
        if success:
            img = detector.find_pose(img)
            pose_data = detector.find_position(img)

            # Check pose_data
            print(pose_data)

            # Create device
            tracker1 = osc.Device(index=1)
            tracker2 = osc.Device(index=2)
            tracker3 = osc.Device(index=3)
            tracker4 = osc.Device(index=4)
            tracker5 = osc.Device(index=5)
            tracker6 = osc.Device(index=6)

            # Set transform of device
            tracker1.set_transform(pose_data[13][1], pose_data[13][2], pose_data[13][3], 0.0, 0.0, 0.0, 0.0)
            tracker2.set_transform(pose_data[14][1], pose_data[14][2], pose_data[14][3], 0.0, 0.0, 0.0, 0.0)
            tracker3.set_transform(pose_data[25][1], pose_data[25][2], pose_data[25][3], 0.0, 0.0, 0.0, 0.0)
            tracker4.set_transform(pose_data[26][1], pose_data[26][2], pose_data[26][3], 0.0, 0.0, 0.0, 0.0)
            tracker5.set_transform(pose_data[27][1], pose_data[27][2], pose_data[27][3], 0.0, 0.0, 0.0, 0.0)
            tracker6.set_transform(pose_data[28][1], pose_data[28][2], pose_data[28][3], 0.0, 0.0, 0.0, 0.0)

            # Send device position to VMT
            tracker1.send_osc()
            tracker2.send_osc()
            tracker3.send_osc()
            tracker4.send_osc()
            tracker5.send_osc()
            tracker6.send_osc()

            # FPS count
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            # Show img
            cv2.imshow("Capture1", img)

            # Stop when user press 'ESC'
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                isclosed = 1
                break

        else:
            break

    # Stop When 'isclosed == 1'
    if isclosed:
        break

# Clean
cap.release()
cv2.destroyAllWindows()
