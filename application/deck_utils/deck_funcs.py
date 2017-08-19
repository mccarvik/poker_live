import pdb
from itertools import combinations

VAL_MAP = {
        'A' : 14,
        'K' : 13,
        'Q' : 12,
        'J' : 11,
        '10' : 10,
        '9' : 9,
        '8' : 8,
        '7' : 7,
        '6' : 6,
        '5' : 5,
        '4' : 4,
        '3' : 3,
        '2' : 2
    }

HAND_MAP = {
        0 : 'Hi Card',
        1 : 'Pair',
        2 : 'Two-Pair',
        3 : 'Three of a Kind',
        4 : 'Straight',
        5 : 'Flush',
        6 : 'Full House',
        7 : 'Four of a Kind',
        8 : 'Straight-Flush'
    }

def getCombinations(deck, cards_needed):
    deck = deck._cards
    return list(combinations(deck, cards_needed))

def evaluateWinner(hands):
    # should take in a list and return a list of corresponding outcomes
    max_hand = []
    for h in hands:
        if not max_hand:
            max_hand.append(h)
            continue
        hvh = handVsHand(h, max_hand[0]) 
        if hvh == 1:
            max_hand = [h]
        elif hvh == 0:
            max_hand.append(h)
    
    win_list = []
    for h in hands:
        if h in max_hand:
            if len(max_hand) > 1:
                win_list.append(0)
            else:
                win_list.append(1)
        else:
            win_list.append(-1)
    return win_list
    
    
def handVsHand(h1, h2):
    if h1[0] > h2[0]:
        return 1
    elif h1[0] < h2[0]:
        return -1
    else:
        # if (h1[0] == 1):
        #     pdb.set_trace()
        #     print("")
        for i in range(len(h1[1])):
            if h1[1][i] > h2[1][i]:
                return 1
            elif h1[1][i] < h2[1][i]:
                return -1
            else:
                continue
    return 0
    