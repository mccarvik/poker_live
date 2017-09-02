import json, pdb
from flask import render_template, redirect, url_for, request
from datetime import datetime
from application import app
from connection import create_connection

# Coroutine notes: https://docs.python.org/3/library/asyncio-task.html#coroutines

@app.route('/')
def base():
    return render_template('base.html', title='Player %s' % str(int(request.environ['SERVER_PORT']) - 8079))

@app.route("/action", methods=['GET', 'POST'])
def action():
    """
        Will create a connection with the server, send the action data,
        and wait for a server response. Then collect data for rendering
        template and close the connection until the next action
    """
    
    player_id = str(int(request.environ['SERVER_PORT']) - 8080)
    action = [request.values['action'], request.values['bet'], player_id]
    print(action)
    new_game_state = create_connection(action)
    new_game_state = json.loads(new_game_state)
    new_game_state['player_id'] = player_id
    new_game_state = json.dumps(new_game_state)
    print("This is the new game state: ", new_game_state)
    return new_game_state