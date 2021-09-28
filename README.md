# WebCam-FullTracking
Using webcam to full tracking

Test video below

https://www.youtube.com/watch?v=8labgxufLRM

------

## 1. Installation

- mediapipe 

  https://mediapipe.dev/

  ```
  pip install mediapipe==0.8.6
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
 
 ### Tracker Info

- Neck: 0
- Left Shoulder: 11
- Right Shoulder: 12
- Left Elbow: 13
- Right Elbow: 14
- Left Hand: 15
- Right Hand: 16
- Left Knee: 25
- Right Knee: 26
- Left Foot: 27
- Right Foot: 28
- Waist: 33

Virtual Tracker device will appear with those number.


### OSC signal example

  ```
  28, 1, 0.0, 0.3891516923904419, -0.6161229014396667, 0.1851455122232437, -0.002754349767864161, 0.0021173597423111957, -0.0012568166056554674, 0.9999931753552609
  ```

  OSC port: 39570
  OSC address: /VMT/Room/Unity


  https://gpsnmeajp.github.io/VirtualMotionTrackerDocument/api/

  Please refer to 'OSC Protocol' in the above link
  


## 3. Program Flow

![화면 캡처 2021-09-08 194115](https://user-images.githubusercontent.com/28009059/132495526-ab5d74f3-fc29-48f4-b602-5546665623ab.png)
![instruction](https://user-images.githubusercontent.com/28009059/135018368-f29f8705-2758-4443-95ba-be1ecf22b7d4.jpg)

