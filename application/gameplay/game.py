import sys, pdb
from application.deck_utils.deck import Deck
from application.deck_utils.card import Card
from application.gameplay.player import Player


class Game():
    """
    
    """
    def __init__(self):
        self._start = False
        self._players = []
        self._board = []
        self._deck = Deck()
        self._button = -1
        self._turn = -1
        self._pot = 0
        self._current_bets = [0] * len(self._players)
    
    
    # Need these two for game flow when game first created
    def start_game(self):
        self._start = True
    
    def is_game_start(self):
        return self._start
    
    def reset_hand(self):
        self._deck.initialize()
        self._button += 1
        self._button = self._button % len(self._players)
        self._turn = (self._button + 2) % len(self._players)
        self._pot = 0
        self._current_bets = [0] * len(self._players)
        self.deal_cards()
    
    def deal_board_card(self):
        self._board.append(self._deck.drawRandom())
    
    def deal_cards(self):
        for p in self._players:
            card1 = self._deck.drawRandom()
            card2 = self._deck.drawRandom()
            p.receive_cards([card1, card2])
    
    def add_player(self, player_id, money):
        p = Player(int(player_id), float(money))
        self._players.append(p)
    
    def accept_action(self, action):
        if action[0] == 'j':
            self.add_player(action[2], action[1])
            return self.getSituation()
    
        if action[0] == 's':
            self.reset_hand()
            return self.getSituation()
        
        if action == 'ch':
            pass
    
    def getSituation(self):
        situation = {}
        situation['current_bets'] = self._current_bets
        situation['board'] = self._board
        situation['button'] = self._button
        situation['pot'] = self._pot
        situation['turn'] = self._turn
        situation['players'] = self.playerSituation()
        return situation
    
    def playerSituation(self):
        plys = []
        for p in self._players:
            plys.append(p.info())
        return plys
