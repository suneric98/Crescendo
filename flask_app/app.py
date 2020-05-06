import json
import pickle
import sklearn

from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
import pandas as pd
from forms import songDropDown, artistDropDown

app = Flask(__name__)
app.config['SECRET_KEY'] = "a_secret_key"
Bootstrap(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/line_graph/", methods=["GET","POST"])
def line_graph():
    # df = pd.read_csv('data/line_vis_data.csv')
    # chart_data = df.to_dict(orient='records')
    # chart_data = json.dumps(chart_data, indent=2)
    # data = {"chart_data":chart_data}
    form = artistDropDown()
    with open("data/line_vis_json.json") as f:
        data = json.load(f)
        if form.validate_on_submit():
            artist = form.artists.data
            chart_data = json.dumps(data[artist], indent=2)
            data = {"chart_data":chart_data}
            return render_template("line_graph.html", form=form, data = data)
        # chart_data = json.dumps(data[list(data.keys())[0]], indent=2)
        data = {"chart_data":json.dumps([])}
        return render_template("line_graph.html", form=form, data=data)

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

@app.route("/num_days/", methods=["GET","POST"])
def num_days():
    form = artistDropDown()
    if form.validate_on_submit():
        flash("Worked for {}".format(form.artists.data))
        return redirect("/num_days")
    return render_template("num_days.html", form=form)
    # clf2 = pickle.load(open("data/adaboost_model.sav", 'rb'))
    # params = ['Tempo', 'Valence', 'Danceability', 'Energy', 'Acousticness',
    #    'Artist Followers', 'Artist Popularity', 'Key_0', 'Key_1', 'Key_2',
    #    'Key_3', 'Key_4', 'Key_5', 'Key_6', 'Key_7', 'Key_8', 'Key_9', 'Key_10',
    #    'Key_11', 'Mode_0', 'Mode_1']
    # print("CLF")
    # print(clf2)
    # print(clf2.predict([[0] * len(params)]))

if __name__ == "__main__":
    app.run(debug=True)
