from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
import pandas as pd

artists = sorted(set(pd.read_csv("data/sets/artist_set.csv")["artists"]))
songs = sorted(set(pd.read_csv("data/sets/song_set.csv")["songs"]))

class songDropDown(FlaskForm):
    # songOrArtist = SelectField("Artist", choices=[("Artist","Artist"),("Song","Song")])
    # songs = SelectField("Song", choices=[(song,song) for song in songs])
    song = StringField("Song", validators=[DataRequired()])
    submit = SubmitField("Submit")

class songInput(FlaskForm):
    song = StringField("Song", validators=[DataRequired()])
    artist = StringField("Artist", validators=[DataRequired()])
    submit = SubmitField("Submit")

class artistDropDown(FlaskForm):
    artists = SelectField("Artist", choices=[(artist,artist) for artist in artists])
    submit = SubmitField("Submit")