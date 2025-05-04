from flask import Flask, render_template
from flask import request, Response
from logging.config import dictConfig
import json
import random
import game as tdle
import nh3

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

RUNNING_GAME = tdle.game("kaksi")

@app.route("/")
def hello_world():
    return render_template('base.html')

@app.route("/game/", methods=['GET', 'POST'])
def game_state():
    if request.method == 'POST':
        data = None
        if request.content_length <= 1024:
            data = request.get_data()
            data = data.decode()
            nh3.clean_text(data)
            app.logger.debug(data)
            game_resp = RUNNING_GAME.guess(guess=data)
            return (game_resp[0], 200)
        elif request.content_length > 1024:
            app.register_error_handler("Request too long", 413)
        else:
            app.register_error_handler("No content length", 411)
    else:
        if RUNNING_GAME:
            return json.dumps(RUNNING_GAME.get_game_state())
        else:
            return ("No game yet", 200)

@app.route("/newgame/", methods=['POST'])
def new_game():
    if request.method == 'POST':
        data = None
        if request.content_length <= 1024:
            data = request.get_data()
            data = data.decode()
            nh3.clean_text(data)
            app.logger.debug(data)
            game_resp = RUNNING_GAME.reset(guess=data)
            return (game_resp[0], 200)
        elif request.content_length > 1024:
            app.register_error_handler("Request too long", 413)
        else:
            app.register_error_handler("No content length", 411)
    else:
        return ("Use POST", 400)