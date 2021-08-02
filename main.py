import cv2
import time
import pose_module as pm


def main(input):
    # Video Capture
    cap = cv2.VideoCapture(input)
    while True:
        # Variables for check FPS
        p_time = 0
        # Variable to check if the user has canceled the program
        is_closed = 0

        # pose_module start
        detector = pm.PoseDetector()
        while True:
            cap.grab()
            success, frame = cap.retrieve()
            # success, frame = cap.read()
            # If video capture was successful
            if success:
                # Get frame that drawn pose estimation and tracker data
                frame = detector.set_pose_data(frame)

                # FPS count
                c_time = time.time()
                fps = 1 / (c_time - p_time)
                p_Time = c_time

                # Put FPS count on frame
                cv2.putText(frame, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

                # Show img
                cv2.imshow("Capture1", frame)

                # Stop when user press 'ESC'
                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    isclosed = 1
                    break

            # Stop When 'isclosed == 1'
            if isclosed:
                break

    # Retrieve resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # ip camera test
    #main('http://172.30.1.7:8080/videofeed')

    # video test
    main('Examples/2.mp4')

    # webcam test
    #main(0)
