import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import json
import pandas as pd

scope = 'playlist-read-private playlist-read-collaborative user-library-read user-read-recently-played user-top-read'
redirect_uri = "http://localhost/"
username = "sonishono"
client_id = "0d7b67f12555488ba8103182d52b85a1"
client_secret = "02e70c1f4df44262a7af61794ff896a7"
jsonPrettify = lambda x: json.dumps(x, indent=2)

class Spotify():
    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
    sp = spotipy.Spotify(auth=token)

    def __init__(self):
        self.token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
        self.sp = spotipy.Spotify(auth=self.token)

    def getFeats(self, songName, artistName):
        songName = songName.strip().lower()
        artistName = artistName.strip().lower()
        query = "track:" + songName + " "+ "artist:" + artistName
        results = self.sp.search(q=query, type="track")
        items = results["tracks"]["items"]
        if len(items) == 0:
            return {}

        song = items[0]
        id = song["id"]
        artistId = ""
        for artist in song["artists"]:
            if artist["name"].lower() == artistName:
                artistId = artist["id"]
        if artistId == "":
            return {}

        songFeats = ['tempo', 'valence', 'danceability', 'energy', 'acousticness', 'key', 'mode']
        feats = []
        audioFeats = self.sp.audio_features(id)[0]
        artistFeats = self.sp.artist(artistId)
        for f in songFeats:
            feats.append(audioFeats[f])
        artistFeats = self.sp.artist(artistId)
        feats.append(artistFeats["followers"]["total"])
        feats.append(artistFeats["popularity"])
        allFeats = ['tempo', 'valence', 'danceability', 'energy', 'acousticness', 'key', 'mode', "followers","popularity"]
        result = {}
        for name,feat in zip(allFeats,feats):
            result[name] = feat
        return result