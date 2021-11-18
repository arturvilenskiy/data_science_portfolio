class Player:
    def __init__(self, name, score=0, hand='None'):
        self.name = name
        self.hand = hand
        self.score = score
    
    def won(self):
        self.score += 1
    
    def assign_hand(self, hand):
        self.hand = hand
    