import pdb
from application.deck_utils.card import Card

class Deck():
    ''' Class to represent a deck of cards '''
    
    SUITS = ['s', 'h', 'c', 'd']
    VALUES = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    
    def __init__(self):
        self.initialize()
    
    def initialize(self):
        self._cards = []
        for s in self.SUITS:
            for v in self.VALUES:
                self._cards.append(Card(v,s))
    
    def drawRandom(self):
        pass

    def removeCards(self, cards):
        for c in cards:
            try:
                self._cards.remove(c)
            except:
                print("Card Already Used")
                raise AssertionError
    