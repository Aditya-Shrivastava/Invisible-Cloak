import cv2
import numpy as np
import time

#capture the camera
cap = cv2.VideoCapture(1)

background = 0

kernel = np.ones((3, 3), np.uint8)

#Capture the background
time.sleep(3)
for i in range(60):
      ret, background = cap.read()
background = cv2.flip(background, 1)

#Capture the foreground
while True:
      
      ret, frame = cap.read()

      #Apply Gaussian Blur
      frame = cv2.GaussianBlur(frame, (15, 15), 1)
      img = cv2.flip(frame, 1)
      hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

      #Define upper and lower range for a color
      lower_col = np.array([110,50,50])
      upper_col = np.array([120,255,255])
      mask1 = cv2.inRange(hsv, lower_col, upper_col)

      
      lower_col = np.array([150,150,0])
      upper_col = np.array([200,250,200])
      mask2 = cv2.inRange(hsv, lower_col, upper_col)

      mask1 = mask1 + mask2

      #Applying Morphological Transformations
      mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel, iterations=2)
      mask1 = cv2.dilate(mask1, kernel, iterations=1)

      mask2 = cv2.bitwise_not(mask1)

      bg = cv2.bitwise_and(background, background, mask=mask1)
      fg = cv2.bitwise_and(img, img, mask=mask2)

      output = cv2.addWeighted(fg, 1, bg, 1, 0)

      cv2.imshow("WIZARDRY", output)

      k = cv2.waitKey(5)
      if k == 27:
            break

cap.release()
cv2.destroyAllWindows()
