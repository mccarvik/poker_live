import os, sys
sys.path.append("/usr/local/lib/python3/dist-packages")
sys.path.append("/usr/local/lib/python3.4/dist-packages")
from flask import Flask

app = Flask(__name__)
app.debug = True
app.secret_key = 'randomstuff'