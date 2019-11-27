import cv2 
import numpy as np 
import sys 
import os 

cascade_path = 'C:/Users/BZL/AppData/Local/Programs/Python/Python36/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml' 
cascade = cv2.CascadeClassifier(cascade_path)
images = os.listdir("data/fairface") 
for image in images: 
    im = cv2.imread(os.path.join("data/fairface", image), 1) 
    rects = cascade.detectMultiScale(im, 1.3, 5) 
    print("detected face", len(rects) )
    if len(rects) == 0: 
        cv2.namedWindow('Result', 0) 
        cv2.imshow('Result', im) 
        os.remove(os.path.join("data/fairface", image)) 
        k = cv2.waitKey(0) 
        if k == ord('q'): 
            break
