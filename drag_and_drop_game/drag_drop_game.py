import cv2
from cvzone.HandTrackingModule import HandDetector

def pinch(lmList):
    thumb_tip = lmList[4]
    index_tip = lmList[8]
    middle_tip = lmList[12]

    if thumb_tip[0] - 60 > index_tip[0]:
        print('1')
        return False
    if thumb_tip[0] + 70 < middle_tip[0]:
        print('2')
        return False
    if thumb_tip[1] - 60 > index_tip[1]:
        print('3')
        return False
    if thumb_tip[1] - 70 > middle_tip[1]:
        print('4')
        return False
    return True


def within_bounds(lmlist, location):
    if lmlist[4][0] < location[0][0] or lmlist[4][0] > location[1][0]:
        return False
    if lmlist[4][1] < location[0][1] or lmlist[4][1] > location[1][1]:
        return False
    return True


def change_in_location(lmlist, location):
    x1_change = lmlist[4][0] - location[0][0]
    y1_change = lmlist[4][1] - location[0][1]
    x2_change = location[1][0] - lmlist[4][0]
    y2_change = location[1][1] - lmlist[4][1]
    return [(x1_change, y1_change), (x2_change, y2_change)]


def move_figure(frame, lmlist, location):
    pinch_loc = (lmlist[4][0], lmlist[4][1])
    cv2.circle(frame, pinch_loc, 10, (0, 0, 255), -1)
    cv2.rectangle(frame, location[0], location[1], (255, 0, 255), -1)
    


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1290)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    moved = False
    pinch_continue = False
    location = [(400,400), (600, 600)]
    while True:
        success, frame = cap.read()
        hands = detector.findHands(frame, draw=False)
        if not moved:
            cv2.rectangle(frame, location[0], location[1], (255, 0, 255), -1)
        if hands:
            hand = hands[0]
            lmList = hand['lmList']
            if pinch(lmList) and within_bounds(lmList, location):
                if not pinch_continue:
                    pinch_continue = True
                    changes = change_in_location(lmList, location)  
                moved = True
                location = [(lmList[4][0] - changes[0][0], lmList[4][1] - changes[0][1]), (lmList[4][0] + changes[1][0], lmList[4][1] + changes[1][1])]
                move_figure(frame, lmList, location)
                """ pinch_loc = (lmList[4][0], lmList[4][1])
                cv2.circle(frame, pinch_loc, 10, (0, 0, 255), -1) """
            else:
                moved = False
                pinch_continue = False
        else:
            moved = False
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()