import json, pdb
from flask import render_template, redirect, url_for, request
from datetime import datetime
from application import app
from connection import create_connection

# Coroutine notes: https://docs.python.org/3/library/asyncio-task.html#coroutines

@app.route('/')
def base():
    return render_template('base.html', title='Texas Hold\'em')

@app.route("/action")
def action(cur_game_state='test'):
    """
        Will create a connection with the server, send the action data,
        and wait for a server response. Then collect data for rendering
        template and close the connection until the next action
    """
    new_game_state = create_connection(cur_game_state)
    print("This is the new game state: ", new_game_state)
    return render_template('base.html', title='Texas Hold\'em')