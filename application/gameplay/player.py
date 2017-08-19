import sys, pdb

class Player():
    """
    
    """
    def __init__(self, player_id, money):
        self._money = money
        self._id = player_id
        self._cards = []
    
    def receive_cards(self, cards):
        self._cards = cards
    
    def has_cards(self):
        if self._cards:
            return True
        else:
            return False
    
    def fold(self):
        self._cards = []
    
    