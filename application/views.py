import json, pdb
from flask import render_template, redirect, url_for, request
from datetime import datetime
from application import app
from connection import create_connection

# Coroutine notes: https://docs.python.org/3/library/asyncio-task.html#coroutines

@app.route('/')
def base():
    return render_template('base.html', title='Texas Hold\'em')

@app.route("/action", methods=['GET', 'POST'])
def action():
    """
        Will create a connection with the server, send the action data,
        and wait for a server response. Then collect data for rendering
        template and close the connection until the next action
    """
    # pdb.set_trace()
    action = [request.values['action'], request.values['bet'], request.values['player']]
    # action = [request.values['action'], request.values['bet']]
    
    print(action)
    new_game_state = create_connection(action)
    print("This is the new game state: ", new_game_state)
    return render_template('base.html', title='Texas Hold\'em')