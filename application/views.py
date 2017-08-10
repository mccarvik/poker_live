import json, pdb
from flask import render_template, redirect, url_for, request
from datetime import datetime
from application import app

# Coroutine notes: https://docs.python.org/3/library/asyncio-task.html#coroutines

@app.route('/')
def home():
    return render_template('home.html', title='Texas Hold\'em')