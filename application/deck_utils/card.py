import pdb
from application.deck_utils.deck_funcs import VAL_MAP

class Card():
    ''' This class will represent a card and help display it thru debugging process'''
    def __init__(self, val, suit):
        ''' Constructor
            
            Parameters
            ==========
            val : str
                represents the rank of the card
            suit : str
                represents the suit of the card
            
            Return
            ======
            NONE
        '''
        self._val = val
        self._suit = suit
    
    def __str__(self):
        ''' returns string representation of class'''
        return (self._val+self._suit)
    
    def __repr__(self):
        ''' returns debugging representation of class'''
        return (self._val+self._suit)
    
    def __eq__(self, other):
        ''' checks equality between one card and another'''
        if (self._val == other._val and self._suit == other._suit):
            return True
        else:
            return False
    
    def __gt__(self, other):
        if (VAL_MAP[self._val] > VAL_MAP[other._val]):
            return True
        else:
            return False
            
    def __lt__(self, other):
        if (VAL_MAP[self._val] < VAL_MAP[other._val]):
            return True
        else:
            return False