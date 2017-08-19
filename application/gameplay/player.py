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
    
    def info(self):
        if self.has_cards():
            return [self._id, self._money, str(self._cards[0]), str(self._cards[1])]
        else:
            return [self._id, self._money, None, None]
    
    