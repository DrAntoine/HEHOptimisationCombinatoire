import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objects as go

"""

Attention, ce script requière les librairies plotly et dash ! 

"""


filePath = "../../../logs_score.txt"
X = []
best = []
mean = []
worst = []

last_update = 0

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id="live-graph", animate=True),
        dcc.Interval(id="graph-update", interval=10000, n_intervals=0),
    ]
)

@app.callback(
    Output("live-graph", "figure"),
    [ Input("graph-update", "n_intervals") ]
)

def update_graph_scatter(n):
    count = 0
    X.clear()
    best.clear()
    mean.clear()
    worst.clear()
    X.append(0)
    best.append(0)
    mean.append(0)
    worst.append(0)
    with open(filePath, "r") as logs:
        for line in logs:
            count +=1
            X.append(count)
            values = line.split("\t")
            values[2] = values[2][:-1]
            best.append(int(values[0]))
            mean.append(int(values[1]))
            worst.append(int(values[2]))

    data_best = plotly.graph_objs.Scatter(
        x = list(X),
        y = best,
        name="Meilleur score de la génération",
        mode = "lines+markers"
    )

    data_mean = plotly.graph_objs.Scatter(
        x = list(X),
        y = mean,
        name="Score moyen de la génération",
        mode = "lines"
    )

    data_worst = plotly.graph_objs.Scatter(
        x = list(X),
        y = worst,
        name="Pire score de la génération",
        mode = "lines"
    )

    all_data = best+mean+worst
    return {"data": [data_best, data_mean,data_worst], 
            "layout" : go.Layout(xaxis=dict(
                range=[min(X), max(X)]),
                yaxis=dict(range=[min(all_data), max(all_data)]),
                )}

if __name__ == "__main__":
    last_update = 0
    app.run_server()