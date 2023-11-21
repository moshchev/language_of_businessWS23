import numpy as np
import pandas as pd
import streamlit as st
from data_retrival import *

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

    # Append the DataFrame and input to the session state
    st.session_state['submissions'].append({
        'input': user_input, 
        'result': result_df,
        'net_income': net_income,
        'gross_margin_rate':gross_margin_rate,
        'fcf_to_revenue': fcf_to_revenue,
        'cash_conversion_rate': cash_conversion_rate,
        'dso':dso
    })
    st.session_state['compare_mode'] = False

initialise_session_state()
# App main interface
# header
st.title('Data Processing App')
# Sidebar for input and submission
user_input = st.sidebar.text_input("Enter ticker of a company", "")
submit_button = st.sidebar.button('Submit', on_click=handle_submission)

submission1 = submission2 = selected_view = selected_submission= None # initialise empty vars for the comparisson mode

# Dropdown for selecting a company to view
if st.session_state.get('submissions'):
    view_options = [submission['input'] for submission in st.session_state['submissions']]
    selected_view = st.sidebar.selectbox('Select a company to view', view_options, key='selected_view')
    selected_submission = next((sub for sub in st.session_state['submissions'] if sub['input'] == selected_view), None)

# Reset comparison mode when a new company is selected to view
if selected_view and st.session_state.get('compare_mode'):
    st.session_state['compare_mode'] = False

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


#-------------------------------------DISPLAY LOGIC--------------------------#
# check if compare mode activated
# if yes -> it will display side by side comparisson #TODO -> replace it with overlapping graphs
# if not -> it will display one selected company 

if st.session_state.get('compare_mode'):
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Ticker: {submission1['input']}")
        st.write("Result:")
        st.dataframe(submission1['result'])
        st.dataframe(submission1['net_income'])

    with col2:
        st.write(f"Ticker: {submission2['input']}")
        st.write("Result:")
        st.dataframe(submission2['result'])
        st.dataframe(submission2['net_income'])

else:
    # Show the selected submission if not in comparison mode
        if selected_submission:
            st.write(f"Input: {selected_submission['input']}")
            st.write("Result:")
            st.dataframe(selected_submission['result'])
            st.write('Net Income')
            st.dataframe(selected_submission['net_income'])
            st.write('Gross Margin Rate')
            st.dataframe(selected_submission['gross_margin_rate'])
            st.write('DSO')
            st.dataframe(selected_submission['dso'])
            

