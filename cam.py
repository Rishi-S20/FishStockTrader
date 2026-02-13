import cv2
import numpy as np
import time
import randStock

cap = cv2.VideoCapture(0)
last_check = time.time()
start_time = time.time()
RUN_DURATION = 60  
CHECK_INTERVAL = 5  
leftCounter = 0
rightCounter = 0
winner = ""


frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))


rightStock = randStock.getRandStock()
leftStock = randStock.getRandStock()

while True:


    if time.time() - start_time >= RUN_DURATION:
        print("1 minute elapsed. Stopping...")
        break

    
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)

        M = cv2.moments(largest)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
            cv2.putText(frame, f"({cx}, {cy})", (cx + 15, cy - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            if time.time() - last_check >= CHECK_INTERVAL:
                if (cx > (frame_width/2) ):
                    rightCounter+=1
                if (cx < (frame_width/2)):
                    leftCounter+=1
                last_check = time.time()
 
    cv2.imshow('Original Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Exiting...")

if leftCounter > rightCounter:
    print("left wins: " + winner)
    winner = leftStock
if rightCounter > leftCounter:
    winner = rightStock
    print("right wins: " + winner)