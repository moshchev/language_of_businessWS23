import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
from data_retrival import *

@st.cache_data
def get_chart_83992296():
    import plotly.graph_objects as go

    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = ["relative", "relative", "total", "relative", "relative", "total"],
        x = ["Sales", "Consulting", "Net revenue", "Purchases", "Other expenses", "Profit before tax"],
        textposition = "outside",
        text = ["+60", "+80", "", "-40", "-20", "Total"],
        y = [60, 80, 0, -40, -20, 0],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
            title = "Profit and loss statement 2018",
            showlegend = True
    )


    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)


get_chart_83992296()