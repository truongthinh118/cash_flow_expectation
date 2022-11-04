import pandas as pd
import numpy as np
import numpy_financial as npf
import streamlit as st

@st.experimental_memo
def expect_fv(expire, banks, rates, periods, pv, pmt):
    df = pd.DataFrame()
    result = []

    for i in range(len(banks)):
        bank = banks[i]
        period = periods[i]

        if (banks.count(bank) > 1):
            banks[i] += "_"+period
            index = banks.index(bank)
            banks[index] += "_"+periods[index]
        period = int(str(period)[0:2])

        rate = rates[i]
        rate = (rate / 12)*period

        fv = []

        for j in range(expire+1):
            # pre_fv = (pv if j == 0 else fv[j-1])
            tem_fv = fv[j-1] if (j % period != 0) else (pv *
                                                        ((1 + rate)**(j//period)))+pmt
            fv.append(tem_fv)

        result.append(fv)
    df = pd.DataFrame(result).T
    df.columns = banks
    return df


def render_calculate_page():
    saving_tab, loan_tab = st.tabs(['Saving Goal','Loan'])
    
    with saving_tab:
        form = st.form('calculate_saving')
        form.number_input('Expired in - Months:',min_value=1)
        form.number_input('Period - Months:', min_value = 1)
        form.number_input('Saving Goal:')
        form.number_input('Present Amout')
        form.number_input('Rate')

        form.form_submit_button('Calculate')

