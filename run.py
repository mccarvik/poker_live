#!flask/bin/python
import os, sys

# Need this to set up modules
sys.path.append("/home/ubuntu/workspace/poker_live")
sys.path.append("/usr/local/lib/python3.4/dist-packages")
from flask import Flask
from application import app

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=True)
# app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=False)