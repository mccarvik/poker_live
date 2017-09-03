import os, sys, pdb
# Need this to set up modules
sys.path.append("/home/ubuntu/workspace/poker_live")
sys.path.append("/usr/local/lib/python3.4/dist-packages")

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
        self._small_blind = 5
        self._current_bets = [0] * len(self._players)
    
    
    # Need these two for game flow when game first created
    def start_game(self):
        self._start = True
    
    def is_game_start(self):
        return self._start
    
    def reset_hand(self):
        self._deck.initialize()
        self._button = (self._button + 1) % len(self._players)
        self._turn = (self._button + 3) % len(self._players)
        self._pot = 0
        
        self._current_bets = [0] * len(self._players)
        self._current_bets[(self._button + 1) % len(self._players)] = self._small_blind
        self._players[(self._button + 1) % len(self._players)]._money -= self._small_blind
        self._current_bets[(self._button + 2) % len(self._players)] = self._small_blind * 2
        self._players[(self._button + 2) % len(self._players)]._money -= self._small_blind * 2
        
        self.deal_cards()
    
    def deal_board_card(self, num=1):
        for n in range(num):
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
    
        if action[0] == 's':
            self.reset_hand()
        
        if action[0] == 'c':
            self.playerCalled()
        
        if action[0] == 'ch':
            self.playerChecked()
        
        return self.getSituation()
    
    def playerChecked(self):
        if self.isEndOfRound(check=True):
            if self.isEndOfHand():
                pass
            else:
                self.nextRound()
        else:
            self._turn = (self._turn + 1) % len(self._players)
    
    def isEndOfHand(self):
        return False
    
    def nextRound(self):
        self._pot += sum(self._current_bets)
        self._current_bets = [0] * len(self._players)
        self._turn = self.getFirstPlayer()
        if self._board == []:
            self.deal_board_card(3)
        else:
            self.deal_board_card(1)
        
    
    def playerCalled(self):
        # make players current bet = the max bet on the table
        self._players[self._turn]._money -= max(self._current_bets) - self._current_bets[self._turn]
        self._current_bets[self._turn] = max(self._current_bets)
        
        if self.isEndOfRound():
            pass
        else:
            self._turn = (self._turn + 1) % len(self._players)
    
    def getIDsPlayersLeft(self):
        hands = [x for x in self._players if str(x._cards[0]) != '']
        return ([x._id for x in hands])
    
    def getFirstPlayer(self):
        for p in self.getIDsPlayersLeft():
            if p > self._button:
                return p
    
    def getLastPlayer(self):
        if self._board != []:
            for p in self.getIDsPlayersLeft():
                if p <= self._button:
                    last = p
            return last
        else:
            return (self._button + 2) % len(self._players)
    
    def isEndOfRound(self, check=False):
        # Check if a turn is over
        max_bet = self._current_bets
        
        # Case one hand left
        hands = [x for x in self._players if str(x._cards[0]) != '']
        if len(hands) == 1:
            return True
        
        # Case checks all around or big blind checks
        if (check and self._turn == self.getLastPlayer()):
            return True
        
        # Case all calls
        for i in self.getIDsPlayersLeft():
            if self._current_bets[i] != max_bet:
                return False
        
        return True
    
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

if __name__ == '__main__':
    # Simulate the start of a game
    game = Game()
    game.accept_action(['j',1000,0])
    game.accept_action(['j',1000,1])
    game.accept_action(['j',1000,2])
    game.accept_action(['j',1000,3])
    game.accept_action(['s',0,0])
    print(game.getSituation())
    
    pdb.set_trace()
    game.accept_action(['c',0,3])
    game.accept_action(['c',0,0])
    print(game.accept_action(['c',0,1]))
    print(game.accept_action(['ch',0,2]))
    game.accept_action(['ch',0,1])
    game.accept_action(['ch',0,2])
    game.accept_action(['ch',0,3])
    print(game.accept_action(['ch',0,0]))
    
    pdb.set_trace()
    print('')