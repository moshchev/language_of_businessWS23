import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
from data_retrival import *

st.set_page_config(layout="wide")
## Initialize session state
if 'submissions' not in st.session_state:
    st.session_state['submissions'] = []

# Handle submission
def handle_submission():
    result_df = get_data(user_input)

    # Append the DataFrame, input, and query name to the session state
    st.session_state.submissions.append({
        "input": user_input, 
        "result": result_df
    })

# App main interface
st.title('Data Processing App')

# User input for query name and query

user_input = st.sidebar.text_input("Enter your input for the query", "")
submit_button = st.sidebar.button('Submit', on_click=handle_submission)

# Create selectbox in siderbar and display the dataframe

if st.session_state.submissions:
    #tab = st.tabs([submission['input'] for submission in st.session_state.submissions])
    option = st.sidebar.selectbox(
     'selcet your company',
     ([submission['input'] for submission in st.session_state.submissions]))
    for i, submission in enumerate(st.session_state.submissions):
        if option == submission['input']:
            st.write(f"Input: {submission['input']}")
            st.write("Result:")
            st.dataframe(submission['result'])


######################## input the value 

# 1. Metrics 1 --making net income for profitability
M1_cok = np.array([0.2218863361547763, 0.2527745440434614, 0.23465802386866177,
        0.23936027478130198], dtype=object)
M1_pep = np.array([0.10313454949532364, 0.09585524825729169, 0.10117660433126811,
        0.10890248805110109], dtype=object)
st.write(M1_cok)
#2. Metrics 2 --gross margin rate also for profitability
M2_cok = np.array([[0.5814342851827737, 0.6027163368257664, 0.5931120130853578,
        0.6077121236515859]], dtype=object)
M2_pep = np.array([[0.5303268821187147, 0.5334952311447769, 0.5481583584380151,
        0.5513467637468173]], dtype=object)
st.write(M2_cok)
#3. Metrics 3 --Free Cash Flow to Total Revenue
M3_cok = np.array([[0.22170030694819087, 0.29124304747121976, 0.26252498939843705,
        0.22586271668545055]], dtype=object)
M3_pep = np.array([[0.0648671173256783, 0.08796587563228225, 0.09056158699482748,
        0.08065692887241108]], dtype=object)

#3. Metrics 3--Cash Conversion Rate
M31_cok = np.array([[1.154684552504716, 1.2920888343055983, 1.2706854266167549,
        1.1738789237668161]], dtype=object)
M31_pep = np.array([[1.2133557800224466, 1.5248096613284328, 1.4905898876404495,
        1.3192507519824994]], dtype=object)

#4. Metrics 4-- solvency:leverage ratio debt-to-equity ratio
M4_cok = np.array([[0.730201066885515, 0.828813986393503, 0.9615756241152282,
        0.9803980008253473]], dtype=object)
M4_pep = np.array([[0.7355787333383538, 0.775012970044002, 0.9053067585301837,
        0.6899459971169776]], dtype=object)

#5. Calculate DSO
M5_cok = np.array([[29.295414380057668, 30.9941792782305, 38.79263342824257,
        38.360972468201574]], dtype=object)
M5_pep = np.array([[39.2598851745532, 38.6934091652616, 41.50343886773148,
        41.92790458748381]], dtype=object)

#6. Calculate ITO
# question? why there only three value by coke?
M6_cok = np.array([[76.47, 78.29654229341669, 89.04191170996799, 83.20952185512006]],
      dtype=object)
M6_pep = np.array([[42.44923107255521, 41.35994605529332, 42.513444664591,
        39.8805256869773]], dtype=object)

#6. Calculate DPO
M61_cok = np.array([[303.68, 301.9808556358664, 300.9201220873967, 278.56351323619947]],
      dtype=object)
M61_pep = np.array([[197.54041798107255, 197.84706675657452, 210.2066232663459,
        209.56989247311827]], dtype=object)

#7.  Calculate Assets Turnover Rate
M7_cok = np.array([[0.45964824147458544, 0.42559867877786955, 0.3801769952267715,
        0.43141431564811705]], dtype=object)
M7_pep = np.array([[0.9361739017359831, 0.857810518362611, 0.8208322398157059,
        0.8550422040307077]], dtype=object)

#8. Calculate the Current Ratio
M8_cok = np.array([[1.1453559115798013, 1.130075187969925, 1.317717964522978,
        0.7567196826456086]], dtype=object)
M8_pep = np.array([[0.8041441105096135, 0.8307780320366133, 0.9841263049803183,
        0.8623723180685205]], dtype=object)

#9. Calculate the interest coverage ratio---Solvency
M9_cok = np.array([[14.249433106575964, 8.780212899185974, 7.784272790535838,
        12.40169133192389]], dtype=object)
M9_pep = np.array([[12.400425985090521, 6.271604938271605, 9.039893617021276,
        9.204405286343613]], dtype=object)

date = ['12.2022','12.2021','12.2020','12.2019']
######################## visulation part


chart_data = pd.DataFrame(M1_cok,index= date)

#rst.header('pie chart')
import plotly.express as px
df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
fig = px.pie(df, values='pop', names='country', title='Population of European continent')

df = pd.DataFrame(dict(
    r=[1, 4.5, 2.3, 2, 3],
    theta=['processing cost','mechanical properties','chemical stability',
           'thermal stability', 'device integration']))
fig1 = px.line_polar(df, r='r', theta='theta', line_close=True)
#st.plotly_chart(fig1)


col1, col2, col3 = st.columns(3)
with col1:
    st.write("""#### Lists of movies filtered by year and Genre """)
    st.area_chart(chart_data)

with col2:
    st.write("""#### User score of movies and their genre """)
    st.bar_chart(chart_data)
    st.write('t\n t\n t\n')

with col3:
    st.plotly_chart(fig,True)

col1, col2, col3 = st.columns(3)
with col1:
    st.write("""#### Lists of movies filtered by year and Genre """)
    st.line_chart(chart_data)

with col2:
    st.write("""#### User score of movies and their genre """)
    st.plotly_chart(fig1,use_container_width=True)

with col3:
    #show numbers
    st.header('display some numbers')
    st.header('test value $100')