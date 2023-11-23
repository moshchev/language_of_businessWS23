import numpy as np
import pandas as pd
import streamlit as st
from data_retrival import *
import plotly.graph_objects as go

def plot_ccc_trend(chart_data, year):
    chart_data['ccc'] = chart_data['dso'] + chart_data['ito'] - chart_data['dpo']
    data = chart_data.loc[year]
    # Define measures for waterfall chart
    measures = ['relative', 'relative', 'relative', 'total']
    # Create a Waterfall chart
    fig = go.Figure(go.Waterfall(
        name="Cash Conversion Cycle",
        orientation="v",
        measure=measures,
        x=['DSO', 'ITO', '-DPO', 'CCC'],
        textposition="outside",
        y=[data['dso'], data['ito'], -data['dpo'], data['ccc']],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    fig.update_layout(
        title=f"Cash Conversion Cycle (CCC) in {year}",
        showlegend=True
    )
    return fig


st.set_page_config(layout="wide")
#------ INIALISAION OF APP
# create session state -> will st.session_state can store data inside of it
def initialise_session_state():
    if 'submissions' not in st.session_state:
        st.session_state['submissions'] = []
    if 'compare_mode' not in st.session_state:
        st.session_state['compare_mode'] = False


# Handle submission -> after the button is clicked, retrived data is stored
# TODO check if it makes sence to save computed metrics in cache as well

def handle_submission():
    result_df = get_data(user_input)

    # compute key metrics of a company
    net_income = get_rate(result_df,'Net Income', 'Total Revenue', 'is', 'is')
    gross_margin_rate = get_rate(result_df,'Gross Profit', 'Total Revenue', 'is', 'is')
    fcf_to_revenue = get_rate(result_df, 'Free Cash Flow', 'Total Revenue', 'cf', 'is')
    cash_conversion_rate = get_rate(result_df, 'Operating Cash Flow', 'Net Income', 'cf', 'is')
    dso = get_rate(result_df, 'Accounts Receivable MA', 'Total Revenue', 'bs', 'is', year=True)
    ito = get_rate(result_df, "Inventory MA","Cost Of Revenue","bs","is", year=True)
    dpo = get_rate(result_df, "Accounts Payable","Cost Of Revenue","bs","is", year=True)
    assert_Turnover_Rate = get_rate(result_df, "Total Revenue", "Total Assets MA", "is", "bs")
    Current_Ratio =  get_rate(result_df, "Current Assets", "Current Liabilities", "bs", "bs")
    Solvency = get_rate(result_df, "EBIT","Interest Expense","is","is")
    
    Total_Revenue = result_df[(result_df['Financial Indicators']=='Total Revenue')].iloc[:,2:]
    Cost_of_Revenue = result_df[(result_df['Financial Indicators']=='Cost Of Revenue')].iloc[:,2:]
    Gross_Profit = result_df[(result_df['Financial Indicators']=='Gross Profit')].iloc[:,2:]
    Selling = result_df[(result_df['Financial Indicators']=='Selling General And Administration')].iloc[:,2:]
    ebit = result_df[(result_df['Financial Indicators']=='EBIT')].iloc[:,2:]
    Interest_Expense = result_df[(result_df['Financial Indicators']=='Interest Expense')].iloc[:,2:]
    Net_Income = result_df[(result_df['Financial Indicators']=='Net Income')].iloc[:,2:]
    Net_Income_Operations= result_df[(result_df['Financial Indicators']=='Net Income From Continuing Operations')].iloc[:,2:]
    Cash_Flow_Financing = result_df[(result_df['Financial Indicators']=='Cash Flow From Continuing Financing Activities')].iloc[:,2:]
    Cash_Flow_Investing = result_df[(result_df['Financial Indicators']=='Cash Flow From Continuing Investing Activities')].iloc[:,2:]
    Cash_Flow_Operating = result_df[(result_df['Financial Indicators']=='Cash Flow From Continuing Operating Activities')].iloc[:,2:]
    Changes_In_Cash = result_df[(result_df['Financial Indicators']=='Changes In Cash')].iloc[:,2:]
    # Append the DataFrame and input to the session state
    
    st.session_state['submissions'].append({
        'input': user_input, 
        'result': result_df,
        'net_income': net_income ,
        'gross_margin_rate':gross_margin_rate,
        'fcf_to_revenue': fcf_to_revenue,
        'cash_conversion_rate': cash_conversion_rate,
        'dso':dso,
        'ito':ito,
        'dpo':dpo,
        'Asset Turnover Rate':assert_Turnover_Rate,
        "Current_Ratio":Current_Ratio,
        'Solvency':Solvency,
        'Total_Revenue':Total_Revenue,
        'Cost_of_Revenue':Cost_of_Revenue,
        'Gross_Profit':Gross_Profit,
        'Selling':Selling,
        'ebit':ebit,
        'Interest_Expense':Interest_Expense,
        'Net_Income':Net_Income,
        'Net_Income_Operations':Net_Income_Operations,
        'Cash_Flow_Financing':Cash_Flow_Financing,
        'Cash_Flow_Investing':Cash_Flow_Investing,
        'Cash_Flow_Operating':Cash_Flow_Operating,
        'Changes_In_Cash':Changes_In_Cash
    })
    st.session_state['compare_mode'] = False

initialise_session_state()
# App main interface
# header
st.title('Financial Analysis Engine Dashboard')
# Sidebar for input and submission
user_input = st.sidebar.text_input("Enter ticker of a company", "")
submit_button = st.sidebar.button('Submit', on_click=handle_submission)

submission1 = submission2 = selected_view = selected_submission= None # initialise empty vars for the comparisson mode

# # Dropdown for selecting a company to view
if st.session_state.get('submissions'):
    view_options = [submission['input'] for submission in st.session_state['submissions']]
    selected_view = st.sidebar.selectbox('Select a company to view', view_options, key='selected_view')
    selected_submission = next((sub for sub in st.session_state['submissions'] if sub['input'] == selected_view), None)

    # Reset comparison mode when a new company is selected to view
    if selected_view and st.session_state.get('compare_mode') and st.session_state.get('last_view') != selected_view:
        st.session_state['compare_mode'] = False
    st.session_state['last_view'] = selected_view

# Dropdowns and button for comparison mode -> comparisson mode will appear when more than one company will be submitted
if st.session_state.get('submissions') and len(st.session_state['submissions']) > 1:
    st.sidebar.write("----")
    st.sidebar.write("Comparison Mode")
    company1 = st.sidebar.selectbox('Select the first company', view_options, key='company1')
    company2 = st.sidebar.selectbox('Select the second company', view_options, key='company2')
    compare_button = st.sidebar.button('Compare')

    # if you click on the button, it will check whether two companies are not equal and then
    if compare_button and company1 != company2:
        st.session_state['compare_mode'] = True
        submission1 = next((sub for sub in st.session_state['submissions'] if sub['input'] == company1), None)
        submission2 = next((sub for sub in st.session_state['submissions'] if sub['input'] == company2), None)

# Sidebar for selecting a company to view and comparison mode

#-------------------------------------DISPLAY LOGIC--------------------------#
# check if compare mode activated
# if yes -> it will display side by side comparisson #TODO -> replace it with overlapping graphs
# if not -> it will display one selected company 

if st.session_state.get('compare_mode') and submission1 and submission2:
    compare_list = ['gross_margin_rate', 'fcf_to_revenue', 'cash_conversion_rate', 'Asset Turnover Rate', "Current_Ratio", 'Solvency']

    for i, ratio in enumerate(compare_list):
        if i % 3 == 0:
            cols = st.columns(3)

        with cols[i % 3]:
            st.header(ratio)

            # Preparing data for line chart
            sub1_data = submission1[ratio].rename(columns={0: company1})
            sub2_data = submission2[ratio].rename(columns={0: company2})
            sub1_data.columns = [col.split('-')[2] if '-' in col else col for col in sub1_data.columns]
            sub2_data.columns = [col.split('-')[2] if '-' in col else col for col in sub2_data.columns]
            
            # Combining data for chart
            chart_data = sub1_data.T
            chart_data.insert(1, company2, sub2_data.T) 
            chart_data = chart_data.rename(columns={0: company1})

            st.line_chart(chart_data)
    
else:
    # Show the selected submission if not in comparison mode
        if selected_submission:
            st.write(f"Ticker: {selected_submission['input']}")
            st.write('## Waterfall chart')
            time = st.selectbox('Selcet the period',(list(selected_submission['Gross_Profit'].columns)))
            waterfall = go.Figure(go.Waterfall(
                name = "", orientation = "v",
                measure = ["relative", "relative", "total", 
                            "relative", "relative", "total",
                            "relative", "relative", "total"],
                x = ["Total Revenue", "Cost of Revenue", "Gross Profit",
                        "Selling", "Others", "EBIT",
                        "Interest_Expense","Tax","Net Income"],
                textposition = "outside",
                y = [int(selected_submission['Total_Revenue'][time]), -int(selected_submission['Cost_of_Revenue'][time]), 0,
                     -int(selected_submission['Selling'][time]), 
                     -int(selected_submission['Gross_Profit'][time])+int(selected_submission['ebit'][time])+int(selected_submission['Selling'][time]), 0,
                     -int(selected_submission['Interest_Expense'][time]),
                     -int(selected_submission['ebit'][time])+int(selected_submission['Interest_Expense'][time])+int(selected_submission['Net_Income'][time]),0],
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))
            waterfall.update_layout(
                    title = "Profit and loss statement "+time,
                    showlegend = True
            )
            
        
            waterfall1 = go.Figure(go.Waterfall(
                name = "", orientation = "v",
                measure = ["relative", "relative", "relative", "relative", "total"],
                x = ['Net Income Operations','Cash Flow From Continuing Financing Activities',
                     'Cash Flow From Continuing Investing Activities','Cash Flow From Continuing Operating Activities','Changes In Cash'],
                textposition = "outside",
                y = [int(selected_submission['Net_Income_Operations'][time]), 
                     int(selected_submission['Cash_Flow_Financing'][time]),
                     int(selected_submission['Cash_Flow_Investing'][time]), 
                     int(selected_submission['Cash_Flow_Operating'][time]),
                     0],
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))
            waterfall1.update_layout(
                    title = "Cash flow in "+time,
                    showlegend = True
            )
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(waterfall, theme="streamlit",use_container_width=True) 
            with col2:
                st.plotly_chart(waterfall1, theme="streamlit",use_container_width=True) 
            
            ### second row of metrics
            chart_data = selected_submission['dso'].T
            chart_data.rename(columns={0: 'dso'}, inplace=True)
            chart_data.insert(1,'dpo',selected_submission['dpo'].T)
            chart_data.insert(1,'ito',selected_submission['ito'].T)
            st.header("DPO ITO and DSO")
            
            fig = plot_ccc_trend(chart_data, time)
            st.plotly_chart(fig, use_container_width=True)