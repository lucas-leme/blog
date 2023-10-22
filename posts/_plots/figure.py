# set plotly default layout

import plotly.graph_objects as go

PLOTLY_DEFAULT_LAYOUT = go.Layout(
    font=dict(
        family="Lexend",
        size=14,
    ),
    # white background
    paper_bgcolor='white',
    plot_bgcolor='white',
    # remove grid
    xaxis=dict(
        showgrid=False,
    ),
    yaxis=dict(
        showgrid=False,
    ),
    # set default colors
    colorway=['#1083ff', '#068b7f',
              '#dc3545', '#ffc107',
              '#b0e157']
)


def make_fig():
    fig = go.Figure(layout=PLOTLY_DEFAULT_LAYOUT)
    return fig
