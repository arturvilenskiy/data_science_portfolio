import cv2
from player import Player
from cvzone.HandTrackingModule import HandDetector

def game(hands, gesture1, gesture2, player1, player2):
    """Controls the game by calling all helper functions.
    
    This function takes list of hands, two gestures, and two players
    and calles helper method to apply scores to each player depending
    on a gesture.
    """
    assign_hands(hands, player1, player2)
    if player1.hand == 0:
        scoring(gesture1, gesture2, player1, player2)
    else:
        scoring(gesture2, gesture1, player1, player2)

def assign_hands(hands, player1, player2):
    """Helper function that assignes hands to player objects.
    
    This function takes a list of hands and two player objects, and
    assignes hand number to a corresponding player.
    """
    if hands[0]['type'] == 'Right':
        player1.assign_hand(0)
        player2.assign_hand(1)
    else:
        player1.assign_hand(1)
        player2.assign_hand(0)


def gesture(fingers):
    """Returns gesture.
    
    This function takes a list of raised fingers and
    assignes to a particular gesture.
    """
    # since it is not perfect, sometimes it recognises 4 fingers as paper
    if sum(fingers) == 5 or sum(fingers) == 4:
        return 'paper'
    # sometimes it mistakenly recognises thumb as a raised finger
    elif sum(fingers) == 0 or sum(fingers) == 1:
        return 'rock'
    return 'scissors'

def scoring(gesture1, gesture2, player1, player2):
    """Helper function that applies scores to players.
    
    This function takes two gestures and two players, and
    assignes wins according to the standard rock-paper-scissors rules.
    """
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
    """Draws rectangle around the hand and prints the gesture.
    
    This function takes an image, a hand object and hand gesture,
    and adds rectange and gesture on top of the current frame.
    """
    #coordinates of the hand in the moment
    bbox = hand['bbox']
    #following expression is taken from the hand_tracking_module.py
    cv2.rectangle(frame, (bbox[0] - 20, bbox[1] - 20),
                          (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                          (255, 0, 255), 2)
    cv2.putText(frame, hand_gesture, (bbox[0] - 20, bbox[1] - 20),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

def display_score(frame, player1, player2):
    """Prints the names and scores of players.
    
    This function takes a frame, and two player objects and prints
    their names and scores in the top left corner.
    """
    cv2.putText(frame, player1.name + ' ' + str(player1.score), (50, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    cv2.putText(frame, player2.name + ' ' + str(player2.score), (50, 100),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

def main():
    """Main function of the game."""
    player1 = Player('Player 1 (Left)')
    player2 = Player('Player 2 (Right)')
    #boolean that controls if the hands are being tracked
    playing = False
    #creates a video feed and sets its resolution
    cap = cv2.VideoCapture(0)
    cap.set(3, 1290)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.5, maxHands=2)
    while True:
        success, frame = cap.read()
        #finds all hands in the frame, draw is false since we have custom draw()
        hands = detector.findHands(frame, draw=False)
        display_score(frame, player1, player2)
        if hands:
            gesture1 = gesture(detector.fingersUp(hands[0]))
            draw(frame, hands[0], gesture1)
            #if there are two hands, we can run the game
            if len(hands) == 2:
                gesture2 = gesture(detector.fingersUp(hands[1]))
                draw(frame, hands[1], gesture2)
                #runs only if in previous frame there were no hands
                if playing == False:
                    game(hands, gesture1, gesture2, player1, player2)
                    playing = True
        else:
            playing = False
        cv2.imshow('Rock Paper Scissors Game', frame)
        #allows to quit the program by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #ends the video feed, and closes all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()