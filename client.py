import sys, socket, threading
from config import HOST, PORT, send_msg, recv_msgs
from run import create_client

# HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
HOST = HOST
PORT = PORT

def handle_input(sock):
    """ Prompt user for message and send it to server """
    print("Type messages, enter to send. 'q' to quit")
    while True:
        msg = input()  # Blocks
        if msg == 'q':
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            break
        try:
            print('sending msg')
            send_msg(sock, msg)  # Blocks until sent
        except (BrokenPipeError, ConnectionError):
            sys.stdout.flush()
            break

if __name__ == '__main__':
    if len(sys.argv) > 1:
        client_no = sys.argv[1]
    else:
        client_no = 0
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print('Connected to {}:{}'.format(HOST, PORT))
    create_client(client_no)

    # Create thread for handling user input and message sending
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
            for msg in msgs:
                print(msg)
        except ConnectionError:
            print('Connection to server closed')
            sock.close()
            break