import os
from flask import Flask

app = Flask(__name__)
app.debug = True
app.secret_key = 'randomstuff'

from application import views