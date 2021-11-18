import cv2
import numpy
import time
from cvzone.HandTrackingModule import HandDetector

def gesture(fingers):
    if sum(fingers) == 5:
        return 'paper'
    elif sum(fingers) == 0:
        return 'rock'
    return 'scissors'

def draw(frame, hand, detector):
    bbox = hand['bbox']
    cv2.rectangle(frame, (bbox[0] - 20, bbox[1] - 20),
                          (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                          (255, 0, 255), 2)
    cv2.putText(frame, gesture(detector.fingersUp(hand)), (bbox[0] - 20, bbox[1] - 20),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1290)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.5, maxHands=2)

    while True:
        success, frame = cap.read()
        hands = detector.findHands(frame, draw=False)

        if hands:
            for hand in hands:
                draw(frame, hand, detector)
        cv2.imshow('Rock Paper Scissors Game', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.01)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()