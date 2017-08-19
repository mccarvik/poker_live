import asyncio, pdb, time
from config import HOST, PORT, parse_recvd_data, prep_msg

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
        for msg in msgs:
            msg = '{}: {}'.format(self.addr, msg)
            print(msg)
            msg = prep_msg(msg)
            
        # writes to just the player who sent message
        for player in players:
            if player.addr == self.addr:
                # player.transport.write(msg)  # <-- non-blocking
                time.sleep(10)
                player.transport.write(prep_msg('ACK'))

    def connection_lost(self, ex):
        """ Called on client disconnect. Clean up client state """
        print('Client {} disconnected'.format(self.addr))
        players.remove(self)

if __name__ == '__main__':
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