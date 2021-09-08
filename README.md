# WebCam-FullTracking
Using webcam to full tracking

Test video below

https://www.youtube.com/watch?v=8labgxufLRM

------

## 1. Installation

- mediapipe 

  https://mediapipe.dev/

  ```
  pip install mediapipe
  ```

  

- python-osc

  https://github.com/attwad/python-osc

  ```
  pip install python-osc
  ```

  

- VMT (Virtual Motion Tracker)

  https://github.com/gpsnmeajp/VirtualMotionTracker

------

## 2. Output

![Pose Landmarks](https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png)

*We use mediapipe landmark output*

- Osc signal example

  ```
  28, 1, 0.0, 0.3891516923904419, -0.6161229014396667, 0.1851455122232437, -0.002754349767864161, 0.0021173597423111957, -0.0012568166056554674, 0.9999931753552609
  ```

  https://gpsnmeajp.github.io/VirtualMotionTrackerDocument/api/

  Please refer to 'OSC Protocol' in the above link

## 3. Program Flow

![화면 캡처 2021-09-08 194115](https://user-images.githubusercontent.com/28009059/132495526-ab5d74f3-fc29-48f4-b602-5546665623ab.png)

