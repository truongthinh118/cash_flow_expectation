import streamlit as st
from streamlit_option_menu import option_menu

import ReferenceRate as rr
import CalculateFlow as cf


def main():
    st.set_page_config(page_title="Cash Flow Expectation",
                   page_icon="💲", initial_sidebar_state="expanded")

    
    # st.title("Cash Flow Expectation")

    with st.sidebar:
        page = option_menu(None, ['Refer Saving Rate', 'Refer Loan Rate', 'Calculate Tool'], icons=[
                           'bank', 'cash-coin', 'calculator'])

    if page == 'Refer Saving Rate':
        rr.render_reference_saving()
    elif page == 'Refer Loan Rate':
        rr.render_reference_loan()
    elif page == 'Calculate Tool':
        st.balloons()
        cf.render_calculate_page()
    # elif page == 'Calculate Loan':
    #     st.balloons()


main()
