import json

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import pandas as pd

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/line_graph/")
def line_graph():
    df = pd.read_csv('topChartWithFeatures.csv')
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template("line_graph.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
