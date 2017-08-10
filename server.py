import asyncio
from config import HOST, PORT

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