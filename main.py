import cv2
import time
import pose_module as pm
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import os


# If input source is video, keep repeat it before user press esc
def main():
    # Variable to check if the user has canceled the program
    is_closed = 0
    p_time = 0
    panel = None
    while True:
        # Video Capture
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

                # # # Show img
                # cv2.imshow("Capture1", frame)
                img = Image.fromarray(frame)  # Image 객체로 변환
                imgtk = ImageTk.PhotoImage(image=img)  # ImageTk 객체로 변환
                label1.image = imgtk
                label1.configure(image=imgtk)
                # label1.after(10, main)


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



if __name__ == "__main__":
    main_gui = tk.Tk()
    main_gui.title("WebCam-FullTracking")
    main_gui.geometry("920x450+50+50")
    main_gui.resizable(True, True)
    label = tk.Label(main_gui, text="카메라로 움직임을 인식하는 저비용 VR 풀트래킹")  # 라벨 생성
    label.grid(row=0, column=0)
    cap = cv2.VideoCapture('C:/Users/Examples/test1.mp4')
    frame = tk.Frame(main_gui, bg="white", width=720, height=480)  # 프레임 너비, 높이 설정
    frame.grid(row=1, column=0)  # 격자 행, 열 배치
    label1 = tk.Label(frame)
    label1.grid(row=2, column=0)
    action1 = ttk.Button(main_gui, text="시작하기", command=main)
    action1.grid(row=3, column=0)

    action2 = ttk.Button(main_gui, text="정지하기")
    action2.grid(row=4, column=0)

    # os.chdir('C:/Users/Examples')  # 현재 작업 디렉토리 변경

    main_gui.mainloop()

    # ip camera test
    # main('http://172.30.1.58:4747/videofeed')
    # video test
    # main('Examples/test1.mp4')
    # webcam test
    # main(0)
