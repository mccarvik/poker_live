import pdb
import numpy as np
from scipy.stats import mode
from app.deck_utils.deck_funcs import VAL_MAP



class HandRules():
    '''This class will determine what hand a given board and hand combo has'''
    
    def __init__(self, hand):
        hand.sort(key=lambda x: VAL_MAP[x._val], reverse=True)
        self._hand = hand
        self._result = self.getHandResult()
    
    def getHandResult(self):
        ''' Pseudo handler to determine the hand ranking
        
        Parameters
        ==========
        NONE
        
        Return
        ======
        res : tuple
            int representing the hand ranking and a string of the cards used for tie breakers
        '''
        result = self.checkFlush()
        if result:
            # if flush, check if a straight can be made for a straight flush
            result_str = self.checkStraight(result[1])
            if result_str:
                return (8, result_str[1])
            else:
                result = (5, result[1][:5])
        
        result_pairs = self.checkPairs()
        if not result:
            result = result_pairs
        else:
            result = result if result[0] > result_pairs[0] else result_pairs
        
        if result[0] < 4:
            result_str = self.checkStraight()
            result = result_str if result_str else result
        return result
        
    def checkFlush(self):
        max_suit = mode([n._suit for n in self._hand])
        if max_suit[1][0] > 4:
            return (5, [n for n in self._hand if n._suit == max_suit[0][0]])
        else:
            return None
    
    def checkStraight(self, hand=None):
        hand = self._hand if not hand else hand
        hand = [VAL_MAP[h._val] for h in hand]
        hand = list(set(hand))
        hand.sort(reverse=True)
        i = 0
        while i + 4 < len(hand):
            if hand[i] - hand[i+4] == 4:
                return (4, [hand[i]])
            i+=1
        
        # Need this for 5 high straight
        if hand[-1] == 2 and hand[-4] == 5 and hand[0] == 14:
            return (4, [5])
        
        return None
    
    def checkPairs(self):
        hand = self._hand
        mode_card = mode([n._val for n in hand])
        
        if mode_card[1][0] == 4:
            left = [c for c in hand if c._val != mode_card[0][0]]
            return (7, [VAL_MAP[mode_card[0][0]], left[0]])
        elif mode_card[1][0] == 1:
            return (0, self._hand[:5])
        elif mode_card[1][0] == 3:
            trip = mode_card[0][0]
            hand = [h for h in hand if h._val != trip]
            mode_2 = mode([n._val for n in hand])
            if mode_2[1][0] > 1:
                pair = mode_2[0][0]
                return (6, [VAL_MAP[trip], VAL_MAP[pair]])
            else:
                left = hand[:2]
                return (3, [VAL_MAP[trip]] + left)
        elif mode_card[1][0] == 2:
            pair = mode_card[0][0]
            hand = [h for h in hand if h._val != pair]
            mode_2 = mode([n._val for n in hand])
            if mode_2[1][0] > 1:
                pair2 = mode_2[0][0]
                hand = [h for h in hand if h._val != pair2]
                left = hand[0]
                if pair > pair2:
                    return (2, [VAL_MAP[pair], VAL_MAP[pair2], left])
                else:
                    return (2, [VAL_MAP[pair2], VAL_MAP[pair], left])
            else:
                left = hand[:3]
                return (1, [VAL_MAP[pair]] + left)
        return None
        