import pandas as pd
import numpy as np
import numpy_financial as npf
import streamlit as st
import Util as ut


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

        fv = [pv]

        for j in range(1,expire+1):

            # tem_fv = fv[j-1] if j % period != 0 else fv[j-1] * (1 + rate)**(j//period) + pmt

            tem_fv = fv[j-1] if j % period != 0 else npf.fv(rate,j//period,-pmt,-pv)
            fv.append(tem_fv)

        result.append(fv)
    df = pd.DataFrame(result).T
    df.columns = banks
    return df


@st.experimental_memo
def calculate_pmt(expired, banks, rates, periods, pv, fv):
    df = pd.DataFrame({
        'Bank':[],
        'Pmt':[],
        'Deposit Amout':[],
        # 'Return':[]
    })
    

    for i in range(len(banks)):
        bank = banks[i]
        period = periods[i]

        if (banks.count(bank) > 1):
            # banks[i] += "_"+period
            dup_bank_index = ut.get_dup_index(bank,banks)
            for index in dup_bank_index:
                banks[index] += "_"+periods[index]
            
            # index = banks.index(bank)
            
        period = int(str(period)[0:2])

        rate = rates[i]
        rate = (rate / 12)*period

        nper = expired//period
        pmt = npf.pmt(rate, nper, pv, -fv)

        deposit_amout = pv
        for i in range(nper):
            deposit_amout = deposit_amout + npf.pv(rate,nper= i,pmt = 0,fv = -pmt)
        # return_amount = npf.pv(rate,nper = nper,pmt = 0,fv= -fv) - deposit_amout
        # result.append(return_amount)
        df.loc[len(df.index)] = [bank,pmt,deposit_amout]
    return df


def render_calculate_page():
    saving_tab, loan_tab = st.tabs(['Saving Goal', 'Loan'])

    with saving_tab:
        form = st.form('calculate_saving')
        form.number_input('Expired in - Months:', min_value=1)
        form.number_input('Period - Months:', min_value=1)
        form.number_input('Saving Goal:')
        form.number_input('Present Amout')
        form.number_input('Rate')

        form.form_submit_button('Calculate')
