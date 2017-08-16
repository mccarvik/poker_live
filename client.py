#!flask/bin/python
import os, sys, pdb

# Need this to set up modules
sys.path.append("/home/ubuntu/workspace/poker_live")
sys.path.append("/usr/local/lib/python3.4/dist-packages")
from flask import Flask
from application import app

def create_client(i):
    PORT = 8080 + int(i)
    app.run(host=os.getenv('IP', '0.0.0.0'),port=PORT, debug=True)
    # app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=False)
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        client_no = sys.argv[1]
    else:
        client_no = 0
    create_client(client_no)