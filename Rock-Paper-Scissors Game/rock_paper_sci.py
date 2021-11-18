import cv2
from player import Player
import time
from cvzone.HandTrackingModule import HandDetector

def game(hands, gesture1, gesture2, player1, player2):
    assign_hands(hands, player1, player2)
    if player1.hand == 0:
        scoring(gesture1, gesture2, player1, player2)
    else:
        scoring(gesture2, gesture1, player1, player2)

def assign_hands(hands, player1, player2):
    if hands[0]['type'] == 'Right':
        player1.assign_hand(0)
        player2.assign_hand(1)
    else:
        player1.assign_hand(1)
        player2.assign_hand(0)


def gesture(fingers):
    if sum(fingers) == 5 or sum(fingers) == 4:
        return 'paper'
    elif sum(fingers) == 0 or sum(fingers) == 1:
        return 'rock'
    return 'scissors'

def scoring(gesture1, gesture2, player1, player2):
    if gesture1 == 'rock' and gesture2 == 'scissors':
        player1.won()
    elif gesture1 == 'scissors' and gesture2 == 'paper':
        player1.won()
    elif gesture1 == 'paper' and gesture2 == 'rock':
        player1.won()
    elif gesture1 == gesture2:
        pass
    else:
        player2.won()
   
def draw(frame, hand, hand_gesture):
    bbox = hand['bbox']
    cv2.rectangle(frame, (bbox[0] - 20, bbox[1] - 20),
                          (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                          (255, 0, 255), 2)
    cv2.putText(frame, hand_gesture, (bbox[0] - 20, bbox[1] - 20),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

def main():
    player1 = Player('Player 1')
    player2 = Player('Player 2')
    playing = False
    cap = cv2.VideoCapture(0)
    cap.set(3, 1290)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.5, maxHands=2)
    while True:
        success, frame = cap.read()
        hands = detector.findHands(frame, draw=False)
        if hands:
            gesture1 = gesture(detector.fingersUp(hands[0]))
            draw(frame, hands[0], gesture1)
            if len(hands) == 2:
                gesture2 = gesture(detector.fingersUp(hands[1]))
                draw(frame, hands[1], gesture2)
                if playing == False:
                    game(hands, gesture1, gesture2, player1, player2)
                    playing = True
                    print(player1.score, player2.score)
        else:
            playing = False
        cv2.imshow('Rock Paper Scissors Game', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.01)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()