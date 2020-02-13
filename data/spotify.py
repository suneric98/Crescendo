import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import json
import pandas as pd
from time import time
from time import sleep
from random import randint

scope = 'playlist-read-private playlist-read-collaborative user-library-read user-read-recently-played user-top-read'
redirect_uri = "http://localhost/"
username = ""
client_id = ""
client_secret = ""

data = pd.read_csv("2018-2020topchart.csv")

token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
sp = spotipy.Spotify(auth=token)

jsonPrettify = lambda x: json.dumps(x, indent=2)

from string import punctuation

def findSongId(trackName, artistName):
    trackName = trackName.split("(feat.")[0].strip()
    trackName = trackName.replace("'","")
    offset = 0
    while offset < 500:
        try:
            global sp
            results = sp.search(q="track:" + trackName, type="track", limit=10, offset=offset)
        except spotipy.client.SpotifyException:
            token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
            sp = spotipy.Spotify(auth=token)
            results = sp.search(q="track:" + trackName, type="track", limit=10, offset=offset)
        items = results['tracks']['items']
        
        trackId = ""
        for track in items:
            trackId = track["id"]
            for artist in track["artists"]:
                if artist["name"] == artistName and track["popularity"] > 0:
    #                 print(jsonPrettify(track))
                    return trackId
        offset += 10
        sleep(0.5)
    return ""


def getTrackFeats(data, restart=True, startIdx = 0):
    songValues = {}
    allRows = []
    if restart:
        df = pd.DataFrame([], columns=["Artist","Title","Rank","Streams","Date",
                                            "Id","Duration","Time Signature", "Tempo",
                                            "Key", "Mode"," Valence", "Danceability",
                                            "Energy", "Acousticness", "Instrumentalness"])
        with open("topChartWithFeatures.csv","w") as f:
            df.to_csv(f,header=True,index=False)

    start = time()
    dayTime = time()
    allRows = []
    for index in range(startIdx, len(data)):
        row = data.iloc[index]
        artistSong = row["Artist"] + "/:/" + row["Song"]
        rowdata = []
        if artistSong not in songValues:
            song = row["Song"]
            artist = row["Artist"]
            sleep(randint(0,2))
            songId = findSongId(song, artist)
            if songId == "":
                print("Error with: {} by {}".format(song, artist))
                rowdata = (songId, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            else:
                try:
                    global sp
                    features = sp.audio_features(songId)[0]
                except spotipy.client.SpotifyException:
                    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
                    sp = spotipy.Spotify(auth=token)
                    features = sp.audio_features(songId)[0]
                if features == None:
                    print(song, artist, songId, sp.audio_features(songId))
                rowdata = (songId, features["duration_ms"], features["time_signature"],
                        features["tempo"], features["key"], features["mode"], features["valence"],
                        features["danceability"], features["energy"], features["acousticness"], 
                        features["instrumentalness"])
            
            songValues[artistSong] = rowdata
        else:
            rowdata = songValues[artistSong]
        completeRowData = [row["Artist"], row["Song"], row["Rank"], row["Streams"], row["Date"]]
        completeRowData.extend(rowdata)
        allRows.append(completeRowData)
        
        if index % 200 == 0 and not index == 0:
            df = pd.DataFrame(allRows, columns=["Artist","Title","Rank","Streams","Date",
                                            "Id","Duration","Time Signature", "Tempo",
                                            "Key", "Mode"," Valence", "Danceability",
                                            "Energy", "Acousticness", "Instrumentalness"])
            df = df.sort_values(by=["Rank"])
            with open("topChartWithFeatures.csv", "a") as f:
                df.to_csv(f, header=False, index=False)
            allRows = []
            print("Day: {}, Saved Row: {} Time: {}".format(row["Date"], index, time() - dayTime))
            dayTime = time()

    print("Time to complete:{}".format(time() - start))

getTrackFeats(data)