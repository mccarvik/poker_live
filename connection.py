import sys, socket, threading, time
from config import HOST, PORT, send_msg, recv_msgs
from multiprocessing.pool import ThreadPool


# HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
HOST = HOST
PORT = PORT

def handle_input(sock, msg):
    """ Prompt user for message and send it to server """
    # print("Type messages, enter to send. 'q' to quit")
    print("handle input")
    send_msg(sock, msg)  # Blocks until sent
    
    

def create_connection(cur_game_state):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print('Connected to {}:{}'.format(HOST, PORT))

    # Create thread for handling user input and message sending
    # thread = threading.Thread(target=handle_input,
    #                           args=[sock],
    #                           daemon=True)
    
    # pool = ThreadPool(processes=2)
    # async_result = pool.apply_async(recv_msgs, (sock, rest))
    thread = threading.Thread(target=handle_input,
                              args=[sock],
                              daemon=True)
    thread.start()
    rest = bytes()
    addr = sock.getsockname()
    # Loop indefinitely to receive messages from server
    while True:
        try:
            (msgs, rest) = recv_msgs(sock, rest)  # blocks
            print("cant get here")
            for msg in msgs:
                print(msg)
            return msg
        except ConnectionError:
            print('Connection to server closed')
            sock.close()
            break