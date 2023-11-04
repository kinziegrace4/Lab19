from flask import Flask, request, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

# https://www.dataquest.io/blog/last-fm-api-python/
# https://www.last.fm/api/intro
LASTFM_API_KEY = 'a3c735dfd7ec562a596c8a61b6d60254'
USER_AGENT = 'Dataquest'
endpoint = 'http://ws.audioscrobbler.com/2.0/'

headers = {
    'user-agent': USER_AGENT
}

payload = {
    'api_key': LASTFM_API_KEY,
    'method': 'chart.getTopArtists',
    'format': 'json'
}



playlist = []

def store_song(my_song, my_artist):
    playlist.append(dict(
        song=my_song,
        artist=my_artist
    ))

class Playlist(FlaskForm):
    song_title = StringField(
        'Song Title',
        validators=[DataRequired()]
    )
    artist = StringField(
        'Artist',
        validators=[DataRequired()]
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/playlist', methods=['GET', 'POST'])
def pl():
    form = Playlist()
    if form.validate_on_submit():
        store_song(form.song_title.data, form.artist.data)
        return redirect('/view_playlist')
    return render_template('playlist.html', form=form)

@app.route('/view_playlist')
def vp():
    return render_template('vp.html', playlist=playlist)

@app.route('/api', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')

        # Make a request to the Last.fm API to search for tracks
        lastfm_url = 'http://ws.audioscrobbler.com/2.0/'
        params = {
            'method': 'track.search',
            'track': search_query,
            'api_key': LASTFM_API_KEY,
            'format': 'json'
        }
        response = requests.get(lastfm_url, params=params)
        data = response.json()

        # Extract song details and pass them to the template for display
        song_results = data.get('results', {}).get('trackmatches', {}).get('track', [])

        return render_template('api.html', song_results=song_results)

    return render_template('search.html')