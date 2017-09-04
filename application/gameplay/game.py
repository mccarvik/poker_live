import os, sys, pdb
# Need this to set up modules
sys.path.append("/home/ubuntu/workspace/poker_live")
sys.path.append("/usr/local/lib/python3.4/dist-packages")
sys.path.append("/usr/local/lib/python3/dist-packages")

from application.deck_utils.deck import Deck
from application.deck_utils.card import Card
from application.gameplay.player import Player
from application.deck_utils.deck_funcs import evaluateWinner
from application.deck_utils.hand_rules import HandRules


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
        self._board = []
        
        self._current_bets = [0] * len(self._players)
        self._current_bets[(self._button + 1) % len(self._players)] = self._small_blind
        self._players[(self._button + 1) % len(self._players)]._money -= self._small_blind
        self._current_bets[(self._button + 2) % len(self._players)] = self._small_blind * 2
        self._players[(self._button + 2) % len(self._players)]._money -= self._small_blind * 2
        
        self.deal_cards()
    
    def deal_board_card(self, num=1):
        for n in range(num):
            self._board.append(str(self._deck.drawRandom()))
    
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
        
        if action[0] == 'f':
            self.playerFolded()
        
        if action[0] == 'b':
            self.playerBet(action[1])
        
        if action[0] == 'r':
            self.playerBet(action[1])
        
        return self.getSituation()
    
    def playerFolded(self):
        self._players[self._turn]._cards = ''
        if self.isEndOfRound():
            if self.isEndOfHand():
                self.cleanUp()
                self.reset_hand()
            else:
                self.nextRound()
        else:
            self.nextTurn()
    
    def playerChecked(self):
        if self.isEndOfRound(check=True):
            if self.isEndOfHand():
                self.cleanUp()
                self.reset_hand()
            else:
                self.nextRound()
        else:
            self.nextTurn()
    
    def playerCalled(self):
        # make players current bet = the max bet on the table
        self._players[self._turn]._money -= max(self._current_bets) - self._current_bets[self._turn]
        self._current_bets[self._turn] = max(self._current_bets)
        
        if self.isEndOfRound():
            if self.isEndOfHand():
                self.cleanUp()
                self.reset_hand()
            else:
                self.nextRound()
        else:
            self.nextTurn()
    
    def playerBet(self, bet):
        self._players[self._turn]._money -= bet
        self._current_bets[self._turn] += bet
        self.nextTurn()
    
    def isEndOfHand(self):
        if len(self.getIDsPlayersLeft()) == 1:
            return True
        
        if len(self._board) == 5:
            return True
        
        return False
    
    def isEndOfRound(self, check=False):
        # Check if a turn is over
        max_bet = max(self._current_bets)
        
        # Case one hand left
        if len(self.getIDsPlayersLeft()) == 1:
            return True
        
        # Case checks all around or big blind checks
        if (check and self._turn == self.getLastPlayer()):
            return True
        elif (check and max_bet == 0):
            return False
        
        # Case all calls
        for i in self.getIDsPlayersLeft():
            if self._current_bets[i] != max_bet:
                return False
        
        # Case for calls on opening round but no big blind check
        if len(self._board) == 0 and not check and max_bet == self._small_blind * 2:
            return False
        
        return True
    
    def cleanUp(self):
        if len(self.getIDsPlayersLeft()) == 1:
            p_id = self.getIDsPlayersLeft()[0]
        else:
            pdb.set_trace()
            res = []
            for p in self.getIDsPlayersLeft():
                res.append(HandRules(self._players[p]._cards + self._board)._result)
            winner = evaluateWinner(res)
        
        ties = len([x for x in winner if x==0])
        if ties > 0:
            for w, p in zip(winner, self.getIDsPlayersLeft()):
                if w == 0:
                    self._players[p]._money += (sum(self._current_bets) + self._pot) / ties
        else:
            for w, p in zip(winner, self.getIDsPlayersLeft()):
                if w == 1:
                    self._players[p]._money += (sum(self._current_bets) + self._pot)
    
    def nextRound(self):
        self._pot += sum(self._current_bets)
        self._current_bets = [0] * len(self._players)
        self._turn = self.getFirstPlayer()
        if self._board == []:
            self.deal_board_card(3)
        else:
            self.deal_board_card(1)
    
    def nextTurn(self):
        next_t = None
        for i in self.getIDsPlayersLeft():
            if i > self._turn:
                self._turn = i
                return
        self._turn = self.getIDsPlayersLeft()[0]
    
    def getIDsPlayersLeft(self):
        hands = [x for x in self._players if x.has_cards()]
        return ([x._id for x in hands])
    
    def getFirstPlayer(self):
        for p in self.getIDsPlayersLeft():
            if p > self._button:
                return p
    
    def getLastPlayer(self):
        last = ""
        if self._board != []:
            for p in self.getIDsPlayersLeft():
                if p <= self._button:
                    last = p
            if last != "":
                return last
            else:
                return self.getIDsPlayersLeft()[-1]
        else:
            return (self._button + 2) % len(self._players)
    
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
    
    while True:
        action = input("next move:  ").split(" ")
        if action[0] == "q":
            break
        if len(action) == 2:
            action[1] = int(action[1])
        game.accept_action(action)
        print(game.getSituation())
    
    pdb.set_trace()
    print('')