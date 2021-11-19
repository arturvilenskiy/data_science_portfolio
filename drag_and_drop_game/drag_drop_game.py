import cv2
import random
from cvzone.HandTrackingModule import HandDetector

def pinch(lmList):
    thumb_tip = lmList[4]
    index_tip = lmList[8]

    if thumb_tip[0] in range(index_tip[0]-10, index_tip[0]+10):
        return True
    if thumb_tip[1] in range(index_tip[1]-20, index_tip[1]+20):
        return True
    return False


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

def intersection_percentage(figure_location, destination_location):
    destination_area = (destination_location[1][0] - destination_location[0][0]) * (destination_location[1][1] - destination_location[0][1])

    if figure_location[0][0] in range(destination_location[0][0], destination_location[1][0]) and figure_location[0][1] in range(destination_location[0][1], destination_location[1][1]):
        occupied_area = (destination_location[1][0] - figure_location[0][0]) * (destination_location[1][1] - figure_location[0][1])

    elif figure_location[1][0] in range(destination_location[0][0], destination_location[1][0]) and figure_location[0][1] in range(destination_location[0][1], destination_location[1][1]):
        occupied_area = (figure_location[1][0] - destination_location[0][0]) * (destination_location[1][1] - figure_location[0][1])
    
    elif figure_location[1][0] in range(destination_location[0][0], destination_location[1][0]) and figure_location[1][1] in range(destination_location[0][1], destination_location[1][1]):
        occupied_area = (figure_location[1][0] - destination_location[0][0]) * (figure_location[1][1] - destination_location[0][1])
    
    elif figure_location[0][0] in range(destination_location[0][0], destination_location[1][0]) and figure_location[1][1] in range(destination_location[0][1], destination_location[1][1]):
        occupied_area = (destination_location[1][0] - figure_location[0][0]) * (figure_location[1][1] - destination_location[0][1])
    else:
        return 0
    return occupied_area/destination_area*100

def create_figures():
    width = 1290
    height = 720
    fig_x = random.randint(0, 1090)
    fig_y = random.randint(0, 520)

    dest_x = random.randint(5, 1090)
    if dest_x in range(fig_x, fig_x + 200):
        dest_x = random.randint(5, 1090)
    dest_y = random.randint(5, 520)
    if dest_y in range(fig_y, fig_y + 200):
        dest_y = random.randint(5, 520)
    return [(fig_x, fig_y), (fig_x + 200, fig_y + 200)], [(dest_x, dest_y), (dest_x + 200, dest_y + 200)]

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1290)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    moved = False
    pinch_continue = False
    location, destination = create_figures()
    percentage = 0
    while True:
        success, frame = cap.read()
        hands = detector.findHands(frame, draw=False)
        cv2.rectangle(frame, (destination[0][0]-5, destination[0][1] - 5), (destination[1][0] + 5, destination[1][1] + 5), (255, 0, 0), 5)
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
                percentage = intersection_percentage(location, destination)
                cv2.putText(frame, 'Percentage: ' + str(intersection_percentage(location, destination)) + '%', (50, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
            else:
                moved = False
                pinch_continue = False
        else:
            moved = False
        cv2.putText(frame, 'Percentage: ' + str(percentage) + '%', (50, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()