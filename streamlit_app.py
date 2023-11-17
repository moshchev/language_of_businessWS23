import numpy as np
import altair as alt
import pandas as pd
import streamlit as st

st.header('st.write')

st.write(1234)

df = pd.DataFrame({
     'first column': [1, 2, 3, 4],
     'second column': [10, 20, 30, 40]
     })
st.write(df)


st.write('Below is a DataFrame:', df, 'Above is a dataframe.')


df2 = pd.DataFrame(
     np.random.randn(200, 3),
     columns=['a', 'b', 'c'])
c = alt.Chart(df2).mark_circle().encode(
     x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
st.write(c)


st.header('Line chart')

chart_data = pd.DataFrame(
     np.random.randn(10, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

st.header('bar chart')
st.bar_chart(chart_data)

st.header('area chart')
st.area_chart(chart_data)

st.header('pie chart')
import plotly.express as px
import plotly.graph_objects as go
df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
fig = px.pie(df, values='pop', names='country', title='Population of European continent')
#fig = go.Figure(data=[go.Pie(hole=.3)])
st.plotly_chart(fig)

st.sidebar.slider('Select a number:', 0, 10, 5)
option = st.sidebar.selectbox(
     'What is your favorite color?',
     ('Blue', 'Red', 'Green'))

st.write('Your favorite color is ', option)