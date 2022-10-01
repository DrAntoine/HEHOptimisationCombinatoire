import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objects as go

"""

Attention, ce script requière les librairies plotly et dash ! 

"""


filePath = "../logs_score.txt"
X = []
best = []
mean = []
worst = []
ultimate = []

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
    ultimate.clear()
    best.clear()
    mean.clear()
    worst.clear()
    # X.append(0)
    # best.append(0)
    # mean.append(0)
    # worst.append(0)
    with open(filePath, "r") as logs:
        for line in logs:
            count +=1
            X.append(count)
            values = line.split("\t")
            values[2] = values[2][:-1]
            ultimate.append(int(values[0]))
            best.append(int(values[1]))
            mean.append(int(values[2]))
            worst.append(int(values[3]))

    # datas_ultimate = []
    # lastmin=max(worst)
    # for i in ultimate:
    #     if i < lastmin:
    #         datas_ultimate.append(i)
    #         lastmin = i
    #     else:
    #         datas_ultimate.append(lastmin)
    
    data_ultimate = plotly.graph_objs.Scatter(
    x = list(X),
    y = ultimate,
    name="Meilleur score jusqu'à cet instant",
    mode = "lines"
    )

    data_best = plotly.graph_objs.Scatter(
        x = list(X),
        y = best,
        name="Meilleur score de la génération",
        mode = "lines"
    )

    data_mean = plotly.graph_objs.Scatter(
        x = list(X),
        y = mean,
        name="Score median de la génération",
        mode = "lines"
    )

    data_worst = plotly.graph_objs.Scatter(
        x = list(X),
        y = worst,
        name="Pire score de la génération",
        mode = "lines"
    )
    onlybest = True

    if not onlybest:
        all_data = best+mean+worst
        return {"data": [data_best, data_mean,data_worst], 
                "layout" : go.Layout(xaxis=dict(
                    range=[min(X), max(X)]),
                    yaxis=dict(range=[min(min(all_data), 0), max(all_data)]),
                    )}
    else:    
        return {"data": [data_best,data_ultimate], 
                "layout" : go.Layout(xaxis=dict(
                    range=[min(X), max(X)]),
                    yaxis=dict(range=[min(min(ultimate), 0), max(best)]),
                    )}

if __name__ == "__main__":
    last_update = 0
    app.run_server()