import asyncio, pdb, time, json
from config import HOST, PORT, parse_recvd_data, prep_msg
from application.gameplay.game import Game
# from application.gameplay.game import Player

players = []

class PokerServerProtocol(asyncio.Protocol):
    """
    Each instance of class represents a client and the socket
    connection to it
    """
    
    def connection_made(self, transport):
        """ Called on instantiation, when new client connects """
        self.transport = transport
        self.addr = transport.get_extra_info('peername')
        self._rest = b''
        players.append(self)
        print('Connection from {}'.format(self.addr))
    
    def data_received(self, data):
        """
        Handle data as it's received. Broadcast complete messages to all other
        clients

        """
        data = self._rest + data
        (msgs, rest) = parse_recvd_data(data)
        self._rest = rest
        action = msgs[0].decode('utf-8').split(",")
        situation = game.accept_action(action)
        
        for msg in msgs:
            msg = '{}: {}'.format(self.addr, msg)
            print(msg)
            # msg = prep_msg(msg)


        print(situation)
        # If player just joined, wait for someone to push the "start game" button
        if (msgs[0].decode('utf-8').split(",")[0] == 'j' and game.is_game_start()) or \
            msgs[0].decode('utf-8').split(",")[0] == 'w':
            return
        game.start_game()
        # pdb.set_trace()
        # # writes to just the player who sent message
        # for player in players:
        #     if player.addr == self.addr:
        #         # time.sleep(25)
        #         # pdb.set_trace()
        #         player.transport.write(prep_msg(json.dumps(situation)))
        
        # write to all players as they all need to be updated on game state
        for player in players:
            player.transport.write(prep_msg(json.dumps(situation)))

    def connection_lost(self, ex):
        """ Called on client disconnect. Clean up client state """
        print('Client {} disconnected'.format(self.addr))
        players.remove(self)

if __name__ == '__main__':
    game = Game()
    loop = asyncio.get_event_loop()
    # Create server and initialize on the event loop
    coroutine = loop.create_server(PokerServerProtocol,
                                   host=HOST,
                                   port=PORT)
    server = loop.run_until_complete(coroutine)
    # print listening socket info
    for socket in server.sockets:
        addr = socket.getsockname()
        print('Listening on {}'.format(addr))
    # Run the loop to process client connections
    loop.run_forever()