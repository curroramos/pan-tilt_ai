#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 13:15:40 2021

@author: curro
"""
import cv2
import mediapipe as mp
import numpy as np


def get_mano(framergb,frame,x,y):
    #Configuración del reconocimiento de mano.
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils
    #Identifiacion de la mano
    result = hands.process(framergb)
    className = ''
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])
            # Drawing landmarks on frames
            mp.solutions.drawing_utils.draw_landmarks(frame, handslms, mp.solutions.hands.HAND_CONNECTIONS)
        #cv2.line(frame, (landmarks[4][0], landmarks[4][1]),(landmarks[8][0], landmarks[8][1]), (0, 255, 0), 2)    
            posicionX = landmarks[4][0]
            posicionY = landmarks[4][1]
    else :
        posicionX='NaN'
        posicionY='NaN'
            
    return posicionX, posicionY


#Configuracion del reconocimietno facial
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def get_cara(framergb,frame,x,y):
    # For webcam input:
    #cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5) as face_detection:
      # while cap.isOpened():
      #   success, image = cap.read()
      #   if not success:
      #     print("Ignoring empty camera frame.")
      #     # If loading a video, use 'break' instead of 'continue'.
      #     continue
    
      #   # To improve performance, optionally mark the image as not writeable to
      #   # pass by reference.
      #   image.flags.writeable = False
      #   image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(framergb)
    
        # Draw the face detection annotations on the image.
        framergb.flags.writeable = True
      #  framergb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.detections:
          for detection in results.detections:
            mp_drawing.draw_detection(frame, detection)
        # Flip the image horizontally for a selfie-view display.
      #  cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
      #  if cv2.waitKey(5) & 0xFF == 27:
      #    break
      
            posicionX = (detection.location_data.relative_bounding_box.xmin + detection.location_data.relative_bounding_box.width/2)*x
            posicionY = (detection.location_data.relative_bounding_box.ymin + detection.location_data.relative_bounding_box.height/2)*y
        else:
            posicionX = 'NaN'
            posicionY = 'NaN'
            
        #print(posicionX)
        #print(posicionY)
        
    return posicionX, posicionY


def get_color(frame, color):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     #Color rojo
    if color=="red":
         low_color = np.array([165, 150, 84])
         high_color = np.array([180, 255, 255])
         #El rojo tiene 2 máscaras porque en el espacio HSV está dividido en dos tramos.
         low_color2 = np.array([0, 150, 84])
         high_color2 = np.array([25, 255, 255])
    #Color Azul
    if color=="blue":
         low_color = np.array([90, 130, 100])
         high_color = np.array([145, 255, 255])
    #Color Verde
    if color=="green":
         low_color = np.array([35, 130, 100])
         high_color = np.array([80, 255, 255])
     
    color_mask = cv2.inRange(hsv_frame, low_color, high_color)
    if color=="red":
         color_mask2 = cv2.inRange(hsv_frame, low_color2, high_color2)
         color_mask = color_mask+color_mask2
        
    contours, _ = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
     
     
    for cnt in contours:
         (x,y,w,h) = cv2.boundingRect(cnt)
         cv2.rectangle(frame, (x, y), (x+w,y+h), (0, 255, 0), 2)
         centroX = round(x+w/2)
         centroY = round(y+h/2)
         cv2.rectangle(frame, (centroX-2, centroY-2), (centroX+2,centroY+2), (0, 255, 0), 2)
         break
    frame = cv2.flip(frame,1)

    if contours:
         # posicionX = frame.shape[1]/2 - centroX
         # posicionY = frame.shape[0]/2- centroY
          posicionY = centroY
          posicionX = centroX
    else :
        posicionX='NaN'
        posicionY='NaN'
     
    return posicionX, posicionY
    
    



    