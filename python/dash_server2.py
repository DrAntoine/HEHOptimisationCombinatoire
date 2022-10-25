import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objects as go
import math

"""

Attention, ce script requière les librairies plotly et dash ! 

"""


filePath = "../logs_score.txt"

last_update = 0
maxX = 0
lowY, highY = math.inf,0 
app = dash.Dash(__name__)

dataLayout = []

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
    data = []
    dataLayout.clear()
    data.clear()
    maxX = 0
    lowY, highY = math.inf,0 
    with open(filePath, "r") as logs:
        for line in logs:
            count +=1
            values = line.split(" ")
            if int(values[4]) not in dataLayout:
                dataLayout.append(int(values[4]))
                data.append([])
            # print(dataLayout)
            # print(values)
            if highY < int(values[0]):
                highY = int(values[0])
            if lowY > int(values[0]):
                lowY = int(values[0])
            if maxX < int(values[5]):
                maxX = int(values[5])
            try:
                data[dataLayout.index(int(values[4]))].append((int(values[5]), int(values[0])))
            except:
                print(values)
    datasGraph = []

    for i in range(len(dataLayout)):
        xdata = []
        ydata = []
        for d in data[i]:
            xdata.append(d[0])
            ydata.append(d[1])
        fig = plotly.graph_objs.Scatter(
        x = xdata,
        y = ydata,
        name=f"Meilleurs score à l'instant T pour la configuration à {dataLayout[i]}",
        mode = "lines"
        )
        datasGraph.append(fig)
        
    return {"data": datasGraph, 
            "layout" : go.Layout(xaxis=dict(
            range=[0, maxX]),
            yaxis=dict(range=[lowY*0.9, highY*1.1]))}

if __name__ == "__main__":
    last_update = 0
    app.run_server()