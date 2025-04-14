import dash
from dash import html, dcc
import plotly.graph_objs as go
import numpy as np
import random

app = dash.Dash(__name__)

# Simulated metric values
risk_metrics = {
    "VaR Limit": random.randint(0, 100),
    "Liquidity Ratio": random.randint(0, 100),
    "Counterparty Exposure": random.randint(0, 100),
}

def create_gradient_bar(title, value):
    colors = []
    for x in range(0, 101, 5):
        if x < 33:
            colors.append("green")
        elif x < 66:
            colors.append("yellow")
        else:
            colors.append("red")

    bar_fig = go.Figure()

    for i in range(len(colors)):
        bar_fig.add_trace(go.Bar(
            x=[5],
            y=[""],
            base=i * 5,
            orientation='h',
            marker=dict(color=colors[i]),
            showlegend=False,
            hoverinfo='skip'
        ))

    bar_fig.add_trace(go.Scatter(
        x=[value],
        y=[""],
        mode="markers+text",
        marker=dict(color="black", size=12),
        text=[f"{value}"],
        textposition="top center",
        showlegend=False
    ))

    bar_fig.update_layout(
        height=60,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(range=[0, 100], visible=False),
        yaxis=dict(visible=False),
        title=dict(text=title, x=0.5)
    )

    return dcc.Graph(figure=bar_fig, config={"displayModeBar": False})

app.layout = html.Div(
    style={"padding": "40px", "font-family": "Arial"},
    children=[
        html.H1("🎯 Risk Appetite", style={"text-align": "center", "margin-bottom": "40px"}),
        html.Div([
            create_gradient_bar(metric, val) for metric, val in risk_metrics.items()
        ])
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
