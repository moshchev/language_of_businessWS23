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
        y = [60, 20, 0, -40, -20, 0],
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

import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
   {
       "col1": np.random.randn(20),
       "col2": np.random.randn(20),
       "col3": np.random.choice(["A", "B", "C"], 20)
       
   }
)
st.write(chart_data)
st.line_chart(chart_data, x="col1", y="col2", color="col3")

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["col1", "col2", "col3"])
st.write(chart_data)
st.line_chart(
   chart_data, x="col1", y=["col2", "col3"], color=["#FF0000", "#0000FF"]  # Optional
)