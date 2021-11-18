import cv2
import numpy
from cvzone.HandTrackingModule import HandDetector

def gesture(fingers):
    if sum(fingers) == 5:
        return 'paper'
    elif sum(fingers) == 0:
        return 'rock'
    return 'scissors'

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1290)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.5, maxHands=2)

    while True:
        success, frame = cap.read()
        hands = detector.findHands(frame, draw=False)

        if hands:
            hand1 = hands[0]
            bbox1 = hand1['bbox']
            fingers1 = detector.fingersUp(hand1)
            cv2.rectangle(frame, (bbox1[0] - 20, bbox1[1] - 20),
                                  (bbox1[0] + bbox1[2] + 20, bbox1[1] + bbox1[3] + 20),
                                  (255, 0, 255), 2)
            cv2.putText(frame, gesture(fingers1), (bbox1[0] - 20, bbox1[1] - 20),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

            if len(hands) == 2:
                hand2 = hands[1]
                bbox2 = hand2['bbox']
                fingers2 = detector.fingersUp(hand2)
                cv2.rectangle(frame, (bbox2[0] - 20, bbox2[1] - 20),
                                  (bbox2[0] + bbox2[2] + 20, bbox2[1] + bbox2[3] + 20),
                                  (255, 0, 255), 2)
                cv2.putText(frame, gesture(fingers2), (bbox2[0] - 20, bbox2[1] - 20),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.imshow('Rock Paper Scissors Game', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()