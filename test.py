import streamlit as st
from data_retrival import *

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

user_input = st.text_input("Enter your input for the query", "")
submit_button = st.button('Submit', on_click=handle_submission)

# Create tabs for each submission
if st.session_state.submissions:
    tab = st.tabs([submission['input'] for submission in st.session_state.submissions])
    for i, submission in enumerate(st.session_state.submissions):
        with tab[i]:
            st.write(f"Input: {submission['input']}")
            st.write("Result:")
            st.dataframe(submission['result'])