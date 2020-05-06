from json import load, dumps
import pickle
from numpy import exp
from spotify import Spotify

from flask import Flask, render_template, flash, redirect
import pandas as pd
from forms import songDropDown, artistDropDown, songInput

app = Flask(__name__)
app.config['SECRET_KEY'] = "a_secret_key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/line_graph/", methods=["GET","POST"])
def line_graph():
    form = artistDropDown()
    with open("data/line_vis_json.json") as f:
        data = load(f)
        if form.validate_on_submit():
            artist = form.artists.data
            chart_data = dumps(data[artist], indent=2)
            data = {"chart_data":chart_data}
            return render_template("line_graph.html", form=form, data = data)
        # chart_data = dumps(data[list(data.keys())[0]], indent=2)
        data = {"chart_data":dumps([])}
        return render_template("line_graph.html", form=form, data=data)

@app.route("/cluster/")
def cluster():
    df = pd.read_csv("data/TopCharts_clustered.csv")
    chart_data = df.to_dict(orient="records")
    chart_data = dumps(chart_data, indent=2)
    data = {"chart_data":chart_data}
    return render_template("cluster.html", data=data)

@app.route("/artist_cluster/")
def artist_cluster():
    df = pd.read_csv("data/ArtistData_clustered_pca.csv")
    chart_data = df.to_dict(orient="records")
    chart_data = dumps(chart_data, indent=2)
    data = {"chart_data":chart_data}
    return render_template("artist_cluster.html", data=data)

@app.route("/num_days/", methods=["GET","POST"])
def num_days():
    form = songInput()
    if form.validate_on_submit():
        s = Spotify()
        data = s.getFeats(form.song.data, form.artist.data)
        if len(data) == 0:
            error = True
            return render_template("num_days.html", form=form, error=error)
        clf = pickle.load(open("data/adaboost_model.sav", 'rb'))
        numKeys = 12
        numModes = 2
        feats = []
        featNames = ['tempo', 'valence', 'danceability', 'energy', 'acousticness', "followers", "popularity", 'key', 'mode']
        for key in featNames:
            value = data[key]
            if key == "key":
                keys = [0] * numKeys
                keys[value] = 1
                feats.extend(keys)
            elif key == "mode":
                modes = [0] * numModes
                modes[value] = 1
                feats.extend(modes)
            else:
                feats.append(value)
        print("FEATS!")
        print(feats)
        result = exp(clf.predict([feats]))[0]
        print(result)
        return render_template("num_days.html", form=form, result=result)
    return render_template("num_days.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
