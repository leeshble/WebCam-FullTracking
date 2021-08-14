import cv2
import tkinter as tk
import pose_module as pm

p_time = 0
cap = cv2.VideoCapture('http://192.168.0.3:8080/video')

def main():
    main_gui = tk.Tk()
    main_gui.title("WebCam-FullTracking")
    main_gui.geometry("920x450+50+50")
    main_gui.resizable(True, True)
    label = tk.Label(main_gui, text="카메라로 움직임을 인식하는 저비용 VR 풀트래킹")  # 라벨 생성
    label.grid(row=0, column=0)
    frame = tk.Frame(main_gui, bg="white", width=720, height=480)  # 프레임 너비, 높이 설정
    frame.grid(row=1, column=0)  # 격자 행, 열 배치
    label1 = tk.Label(frame)
    label1.grid(row=2, column=0)
    action1 = tk.Button(main_gui, text="시작하기", command=main)
    action1.grid(row=3, column=0)

    action2 = tk.Button(main_gui, text="정지하기")
    action2.grid(row=4, column=0)

    #pm.camera_input('Examples/2.mp4')
    #pm.camera_input(0)
    pm.camera_input()
    main_gui.mainloop()


if __name__ == "__main__":
    main()
    cap.release()
    cap.destroyAllWindows()