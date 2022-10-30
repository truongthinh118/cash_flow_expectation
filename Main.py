import streamlit as st
from streamlit_option_menu import option_menu
import ReferenceRate as rr

st.set_page_config(page_title="Cash Flow Expectation",
                   page_icon="💲", initial_sidebar_state="expanded")


def main():
    st.title("Cash Flow Expectation")

    with st.sidebar:
        page = option_menu(None, ['Refer Saving Rate', 'Refer Loan Rate', 'Calculate Saving Cash Flow', 'Calculate Loan Cash Flow'], icons=[
                           'bank', 'cash-coin', 'piggy-bank', 'credit-card'])

    if page == 'Refer Saving Rate':
        rr.render_reference_saving()
    elif page == 'Refer Loan Rate':
        rr.render_reference_loan()
    elif page == 'Calculate Saving':
        st.balloons()
    elif page == 'Calculate Loan':
        st.balloons()


main()
