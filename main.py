import cv2
import time
import pose_module as pm
import tkinter as tk


# If input source is video, keep repeat it before user press esc
def main(input):
    # Variable to check if the user has canceled the program
    is_closed = 0
    p_time = 0

    while True:
        # Video Capture
        cap = cv2.VideoCapture(input)

        # Variables for check FPS

        # pose_module start
        detector = pm.PoseDetector()
        while True:
            # Get frame
            success, frame = cap.read()
            # If video capture was successful
            if success:
                # Get frame that drawn pose estimation and tracker data
                frame = detector.set_pose_data(frame)

                # Get FPS value
                fps, p_time = fps_count(p_time)

                # Put FPS count on frame
                cv2.putText(frame, str(fps), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

                # Show img
                cv2.imshow("Capture1", frame)

            # Stop when user press 'ESC'
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                is_closed = 1
                break

        # Stop When 'isclosed == 1'
        if is_closed:
            break

    # Retrieve resources
    cap.release()
    cv2.destroyAllWindows()


# FPS count
def fps_count(p_time):
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    return int(fps), c_time


def main_screen():
    main_gui = tk.Tk()
    main_gui.title("WebCam-FullTracking")
    main_gui.geometry("920x450+50+50")
    main_gui.resizable(True, True)
    main_gui.mainloop()


if __name__ == "__main__":
    # ip camera test
    #main('http://192.168.35.204:8080/videofeed')

    # video test
    main('Examples/2.mp4')

    # webcam test
    #main(0)

    #main_screen()