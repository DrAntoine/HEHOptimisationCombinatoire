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
            # values[2] = values[2][:-1]
            ultimate.append(int(values[0]))
            best.append(int(values[1]))
            mean.append(int(values[2]))
            worst.append(int(values[3]))

    datas_ultimate_from_begin = []
    lastmin=max(worst)
    for i in ultimate:
        if i < lastmin:
            datas_ultimate_from_begin.append(i)
            lastmin = i
        else:
            datas_ultimate_from_begin.append(lastmin)
    
    data_ultimate = plotly.graph_objs.Scatter(
    x = list(X),
    y = ultimate,
    name="Meilleur score jusqu'à cet instant pour la configuration",
    mode = "lines"
    )

    data_ultimate_begin = plotly.graph_objs.Scatter(
    x = list(X),
    y = datas_ultimate_from_begin,
    name="Meilleur score jusqu'à cet instant depuis le début",
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

    worstData = False
    medianData = True
    currentBest = True
    configurationBest = True
    sessionBest = True
    
    all_data = []
    datas = []
    
    if worstData:
        datas.append(data_worst)
        all_data += worst
    if medianData:
        datas.append(data_mean)
        all_data += mean
    if currentBest:
        datas.append(data_best)
        all_data += best
    if configurationBest:
        datas.append(data_ultimate)
        all_data += ultimate
    if sessionBest:
        datas.append(data_ultimate_begin)
        all_data += datas_ultimate_from_begin
        
    return {"data": datas, 
            "layout" : go.Layout(xaxis=dict(
            range=[min(X), max(X)]),
            yaxis=dict(range=[min(all_data)*0.9, max(all_data)*1.1]),
            )}

if __name__ == "__main__":
    last_update = 0
    app.run_server()