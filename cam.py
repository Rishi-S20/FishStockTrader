import cv2
import numpy as np
import time
import randStock
import trade

cap = cv2.VideoCapture(0)
last_check = time.time()
start_time = time.time()
RUN_DURATION = 60  
CHECK_INTERVAL = 5  
leftCounter = 0
rightCounter = 0


frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))


rightStock = randStock.getRandStock()
leftStock = randStock.getRandStock()

while True:


    if time.time() - start_time >= RUN_DURATION:
        print("TIME IS UP")
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

winner = None
if leftCounter > rightCounter:
    winner = leftStock
    print(f"Left Stock wins: {winner}")
elif rightCounter > leftCounter:
    winner = rightStock
    print(f"Right Stock wins: {winner}")
else:
    print("Tie")


if winner:
    retries = 0
    while not trade.is_tradeable(winner) and retries < 10:
        print(f"{winner} not tradeable, re-rolling...")
        winner = randStock.getRandStock()
        retries += 1

    if trade.is_tradeable(winner):
        trade.place_trade(winner, amount=100)
    else:
        print("Couldn't find a tradeable stock after 10 tries.")