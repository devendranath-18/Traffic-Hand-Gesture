import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True,
                    min_detection_confidence=0.05, model_complexity=2)
mp_drawing = mp.solutions.drawing_utils


def detectPose(image, pose, display=True):
    output_image = image.copy()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    height, width, _ = image.shape
    landmarks = []
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image=output_image, landmark_list=results.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS)
        for landmark in results.pose_landmarks.landmark:
            landmarks.append(
                (int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))
    if display:
        plt.figure(figsize=[15, 15])
        plt.subplot(122)
        plt.imshow(output_image[:, :, ::-1])
        plt.title("Output Image")
        plt.axis('off')
    else:
        return output_image, landmarks


def calculateAngle(landmark1, landmark2, landmark3):
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360
    return angle


def inRange(angle, min, max):
    if angle < min or angle > max:
        return False
    return True


def VIPSalute(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
    if inRange(left_elbow_angle, 150, 180) and inRange(right_elbow_angle, 0, 45) and inRange(left_shoulder_angle, 75, 120) and inRange(right_shoulder_angle, 75, 120):
        return True

    return False


def Wait(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
    if inRange(left_elbow_angle, 30, 90) and inRange(right_elbow_angle, 250, 350) and inRange(left_shoulder_angle, 85, 150) and inRange(right_shoulder_angle, 85, 150):
        return True
    return False


def RightTurnWaiting(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
    if inRange(left_elbow_angle, 160, 200) and inRange(right_elbow_angle, 0, 20) and inRange(left_shoulder_angle, 90, 150) and inRange(right_shoulder_angle, 85, 130):
        return True
    elif inRange(left_elbow_angle, 130, 200) and inRange(right_elbow_angle, 130, 200) and inRange(left_shoulder_angle, 250, 320) and inRange(right_shoulder_angle, 75, 130):
        return True
    return False


def RightTurn(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
    if inRange(left_elbow_angle, 160, 200) and inRange(right_elbow_angle, 15, 40) and inRange(left_shoulder_angle, 90, 150) and inRange(right_shoulder_angle, 85, 130):
        return True
    elif inRange(left_elbow_angle, 300, 360) and inRange(right_elbow_angle, 150, 200) and inRange(left_shoulder_angle, 80, 130) and inRange(right_shoulder_angle, 75, 130):
        return True
    return False


def LeftTurnWaiting(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
    if inRange(left_elbow_angle, 0, 20) and inRange(right_elbow_angle, 160, 200) and inRange(left_shoulder_angle, 85, 130) and inRange(right_shoulder_angle, 90, 150):
        return True
    elif inRange(left_elbow_angle, 130, 200) and inRange(right_elbow_angle, 130, 200) and inRange(left_shoulder_angle, 75, 130) and inRange(right_shoulder_angle, 250, 320):
        return True
    return False


def LeftTurn(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
    if inRange(left_elbow_angle, 15, 40) and inRange(right_elbow_angle, 160, 200) and inRange(left_shoulder_angle, 85, 130) and inRange(right_shoulder_angle, 90, 150):
        return True
    elif inRange(left_elbow_angle, 150, 200) and inRange(right_elbow_angle, 300, 360) and inRange(left_shoulder_angle, 75, 130) and inRange(right_shoulder_angle, 80, 130):
        return True
    elif inRange(left_elbow_angle, 150, 210) and inRange(right_elbow_angle, 150, 210) and inRange(left_shoulder_angle, 85, 150) and inRange(right_shoulder_angle, 180, 250):
        return True
    return False


def MoveStraight(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
    if inRange(left_elbow_angle, 170, 210) and inRange(right_elbow_angle, 170, 200) and inRange(left_shoulder_angle, 150, 200) and inRange(right_shoulder_angle, 0, 45):
        return True
    elif inRange(left_elbow_angle, 150, 200) and inRange(right_elbow_angle, 160, 200) and inRange(left_shoulder_angle, 60, 110) and inRange(right_shoulder_angle, 0, 30):
        return True
    elif inRange(left_elbow_angle, 160, 200) and inRange(right_elbow_angle, 160, 200) and inRange(left_shoulder_angle, 120, 180) and inRange(right_shoulder_angle, 120, 180):
        return True
    return False


def Stop(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
    if inRange(left_elbow_angle, 170, 200) and inRange(right_elbow_angle, 170, 210) and inRange(left_shoulder_angle, 0, 45) and inRange(right_shoulder_angle, 150, 200):
        return True
    elif inRange(left_elbow_angle, 160, 200) and inRange(right_elbow_angle, 150, 200) and inRange(left_shoulder_angle, 0, 30) and inRange(right_shoulder_angle, 60, 110):
        return True
    elif inRange(left_elbow_angle, 150, 200) and inRange(right_elbow_angle, 160, 220) and inRange(left_shoulder_angle, 70, 120) and inRange(right_shoulder_angle, 140, 180):
        return True
    elif inRange(left_elbow_angle, 160, 220) and inRange(right_elbow_angle, 150, 200) and inRange(left_shoulder_angle, 140, 180) and inRange(right_shoulder_angle, 70, 120):
        return True
    elif inRange(left_elbow_angle, 160, 220) and inRange(right_elbow_angle, 0, 20) and inRange(left_shoulder_angle, 140, 200) and inRange(right_shoulder_angle, 60, 120):
        return True
    elif inRange(left_elbow_angle, 0, 20) and inRange(right_elbow_angle, 160, 220) and inRange(left_shoulder_angle, 60, 120) and inRange(right_shoulder_angle, 140, 200):
        return True
    return False


def classifyPose(landmarks, output_image, display=True):
    label = 'Unknown Pose'
    color = (0, 0, 255)
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])

    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
    if Stop(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
        label = 'STOP'
        color = (0, 255, 0)
    elif Wait(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
        label = 'WAIT'
        color = (0, 255, 0)
    elif LeftTurn(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
        label = 'TURN LEFT'
        color = (0, 255, 0)
    elif RightTurn(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
        label = 'TURN RIGHT'
        color = (0, 255, 0)
    elif LeftTurnWaiting(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
        label = 'WAITING TURN LEFT'
        color = (0, 255, 0)
    elif RightTurnWaiting(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
        label = 'WAITING TURN RIGHT'
        color = (0, 255, 0)
    elif MoveStraight(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
        label = 'MOVE STRAIGHT'
        color = (0, 255, 0)
    elif VIPSalute(left_elbow_angle, right_elbow_angle, left_shoulder_angle, right_shoulder_angle):
        label = 'VIP SALUTE'
        color = (0, 255, 0)

    cv2.putText(output_image, label, (10, 30),
                cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    if display:
        plt.figure(figsize=[10, 10])
        plt.imshow(output_image[:, :, ::-1])
        plt.title("Output Image")
        plt.axis('off')

    else:
        return output_image, label


if __name__ == '__main__':
    pose_video = mp_pose.Pose(static_image_mode=False,
                              min_detection_confidence=0.5, model_complexity=1)
    camera_video = cv2.VideoCapture(0)
    camera_video.set(3, 1280)
    camera_video.set(4, 960)
    cv2.namedWindow('Traffic Sign Classification', cv2.WINDOW_NORMAL)
    while camera_video.isOpened():
        ok, frame = camera_video.read()
        time1 = time()
        if not ok:
            continue
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        frame = cv2.resize(
            frame, (int(frame_width * (640 / frame_height)), 640))
        frame, landmarks = detectPose(frame, pose_video, display=False)
        time2 = time()
        if (time2 - time1) > 0:
            fps = 1.0 / (time2 - time1)
        cv2.putText(frame, 'FPS: {}'.format(int(fps)), (1000, 30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

        time1 = time2
        frame, _ = classifyPose(landmarks, frame, display=False)
        cv2.imshow('Traffic Sign Classification', frame)
        k = cv2.waitKey(1) & 0xFF
        if(k == 27):
            break
    camera_video.release()
    cv2.destroyAllWindows()
