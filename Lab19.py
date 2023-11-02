from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import  DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)


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

@app.route('/playlist', methods=('GET', 'POST'))
def pl():
    form = Playlist()
    if form.validate_on_submit():
        store_song(form.song_title.data, form.artist.data)
        return redirect('/view_playlist')
    return render_template('playlist.html', form=form)

@app.route('/view_playlist')
def vp():
    return render_template('vp.html', playlist=playlist)

