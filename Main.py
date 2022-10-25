import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy_financial as npf
import ReferenceRate as rr

st.set_page_config(page_title="Cash Flow Expectation",
                   page_icon="💲", initial_sidebar_state="expanded")


def main():
    st.title("Cash Flow Expectation")

    with st.sidebar:
        page = option_menu(None, ["Reference Deposit Rate", "Reference Loan Rate", "Calculate Saving", "Calculate Loan"], icons=[
                           'piggy-bank', 'credit-card', 'graph-up', 'graph-down'])

    if page == 'Reference Deposit Rate':
        rr.render_reference_saving()
    elif page == 'Reference Loan Rate':
        rr.render_reference_loan()


main()
