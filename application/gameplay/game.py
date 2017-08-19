import sys,pdb
from application.deck_utils.deck import Deck
from application.deck_utils.card import Card


class Game() {
    """
    
    """
    def __init__(self):
        self._players = []
        self._board = []
        self._deck = Deck()
        self._button = 0
        self._turn = 
        self._pot = 0
        self._current_bets = [0] * len(self._players)
    
    def reset_hand(self):
        self._deck.initialize()
        self._button = self._button % len(self._players)
        self._turn = (self._button + 2) % len(self._players)
        self._pot = 0
        self._current_bets = [0] * len(self._players)
    
    def deal_board_card(self):
        board.append(self.deal_card())
    
    def deal_card(self):
        return deck.drawRandom()
    
    def add_player(self, p):
        self._players.append(p)
    
    def accept_action(self, action, val):
        if action == 'ch':
            pass
    
    def getSituation(self):
        situation = {}
        situation['current_bets'] = self._current_bets
        situation['board'] = self._board
        situation['button'] = self._button
        situation['pot'] = self._pot
}