from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys
import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from client import cid, secret
from main import get_top_tracks, recommendation

app = Flask(__name__)

os.environ['SPOTIPY_CLIENT_ID'] = cid
os.environ['SPOTIPY_CLIENT_SECRET'] = secret
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

auth_manager = SpotifyClientCredentials(client_id=cid,
                                        client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=auth_manager)

username = ""
scope = 'user-top-read playlist-modify-public'
token = util.prompt_for_user_token(username, scope)

time_range = "short_term"

@app.route('/', methods=['POST', 'GET'])
def index():
    if token:
        sp = spotipy.Spotify(auth=token)
        top_tracks = get_top_tracks()
    else:
        print("Can't get token for " + username)
        return render_template('index.html')

    return render_template("index.html", top_tracks=top_tracks, sp=sp)


@app.route('/recs/<string:id>', methods=['GET', 'POST'])
def recs(id):
    recs = recommendation(id)
    return render_template('recs.html', recs=recs, sp=sp)

if __name__ == "__main__":
    app.run(debug=True)