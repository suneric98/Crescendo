import json
import pandas as pd
import json

df = pd.read_csv('topChartWithFeatures.csv')

def makeLineGraphData():
    print(df.shape)
    numDays = {}
    for idx,row in df.iterrows():
        # key = row["Song"] + "/:/" + row["Artist"]
        key = row["Artist"]
        numDays[key] = numDays.get(key, 0) + 1

    rowsToRemove = []
    for idx, row in df.iterrows():
        # key = row["Song"] + "/:/" + row["Artist"]
        key = row["Artist"]
        if numDays[key] < 300:
            rowsToRemove.append(idx)

    df = df.drop(rowsToRemove)
    print(df.shape)
    df.to_csv("line_vis_data.csv", index=False)

def makeLineGraphJson():
    artists = set()
    result = {}
    data = df.to_dict("records")
    for row in data:
        artist = row["Artist"]
        artists.add(artist)
        if artist not in result:
            result[artist] = []
        result[artist].append(row)
    with open("line_vis_json.json", "w") as f:
        json.dump(result, f)


def makeArtistsSongs():
    artists = set()
    songs = set()
    for idx, row in df.iterrows():
        artists.add(row["Artist"])
        songs.add(row["Song"])
    artists = sorted(artists)
    songs = sorted(songs)
    pd.DataFrame({"artists":list(artists)}).to_csv("artist_set.csv", index=False)
    pd.DataFrame({"songs":list(songs)}).to_csv("song_set.csv", index=False)

makeLineGraphJson()
# makeArtistsSongs()