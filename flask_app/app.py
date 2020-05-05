import json

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import pandas as pd

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/line_graph/")
def line_graph():
    df = pd.read_csv('data/line_vis_data.csv')
    songs = set()
    artists = set()
    songDays = {}
    for idx, row in df.iterrows():
        artists.add(row["Artist"])
        songs.add(row["Song"])
        key = row["Song"] + "/:/" + row["Artist"]
        songDays[key] = songDays.get(key,0) + 1
    # artists = json.dumps(list(artists), indent=2)
    # songs = json.dumps(list(songs), indent=2)
    # songDays = json.dumps(songDays, indent=2)
    # data = {"artists":artists,"songs":songs,"songDays":songDays}
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {"chart_data":chart_data}
    return render_template("line_graph.html", data=data)

@app.route("/cluster/")
def cluster():
    df = pd.read_csv("data/TopCharts_clustered.csv")
    chart_data = df.to_dict(orient="records")
    chart_data = json.dumps(chart_data, indent=2)
    data = {"chart_data":chart_data}
    return render_template("cluster.html", data=data)

@app.route("/artist_cluster/")
def artist_cluster():
    df = pd.read_csv("data/ArtistData_clustered_pca.csv")
    chart_data = df.to_dict(orient="records")
    chart_data = json.dumps(chart_data, indent=2)
    data = {"chart_data":chart_data}
    return render_template("artist_cluster.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
