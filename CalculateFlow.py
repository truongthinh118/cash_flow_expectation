import numpy_financial as npf
import pandas as pd
import streamlit as st

import Util as ut


@st.experimental_memo
def calculate_fv(expire, banks, rates, periods, pv, pmt):
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

        for j in range(1, expire+1):

            # tem_fv = fv[j-1] if j % period != 0 else fv[j-1] * (1 + rate)**(j//period) + pmt

            tem_fv = fv[j - 1] if j % period != 0 else npf.fv(rate, j//period, -pmt, -pv)
            fv.append(tem_fv)

        result.append(fv)
    df = pd.DataFrame(result).T
    df.columns = banks
    return df


@st.experimental_memo
def calculate_pmt(expired, banks, rates, periods, pv, fv):
    df = pd.DataFrame({
        'Bank': [],
        'Pmt': [],
        'Deposit Amout': [],
        # 'Return':[]
    })

    for i in range(len(banks)):
        bank = banks[i]
        period = periods[i]

        dup_bank_index = ut.get_dup_index(bank, banks)
        if dup_bank_index is not None and len(dup_bank_index)>1:

            for index in dup_bank_index:
                banks[index] += "_"+periods[index]

        period = int(str(period)[0:2])

        rate = rates[i]
        rate = (rate / 12)*period

        nper = expired//period
        pmt = npf.pmt(rate, nper, pv, -fv)

        deposit_amout = pv
        for j in range(nper):
            deposit_amout = deposit_amout + npf.pv(rate, nper=j, pmt=0, fv=-pmt)
        
        df.loc[len(df.index)] = [banks[i], pmt, deposit_amout]
    return df

@st.experimental_memo
def calculate_loan_pmt(expired, banks, rates, fv_list):
    result = []
    for i in range(len(banks)):
        fv = fv_list[i]
        pmt = fv/expired
        result.append(pmt)
    return result

def render_calculate_page():
    saving_tab, loan_tab = st.tabs(['Saving Goal', 'Loan'])
    
    with saving_tab:
        col1, col2 = st.columns(2)
        with col1:
            form = st.form('calculate_saving')
            expired = form.number_input('Expired in - Months:', min_value=1)
            period = form.number_input('Period - Months:', min_value=1)
            fv = form.number_input('Saving Goal:', step=100, min_value=0)
            pv = form.number_input('Present Amout', step=100, min_value=0)
            rate = form.number_input('Rate', min_value=0.00)

            calculate = form.form_submit_button('Calculate')

        if st.session_state.get('form_submit_button4') != True:
            st.session_state['form_submit_button4'] = calculate

        if st.session_state['form_submit_button4']:
            warning = ut.valid_input(rate,pv,fv,None)
            if warning is not None:
                col2.warning(warning)
            else:
                result = calculate_pmt(expired,['Bank'],[rate/100],[period],pv,fv)
                col2.altair_chart(ut.generate_pmt_chart(result),use_container_width=True)

    with loan_tab:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write('\n')
            st.write('\n')
            form = st.form('calculate_loan')
            expired = form.number_input('Expired in - Months:', min_value=1)
            
            pv = form.number_input('Loan Amout', step=100, min_value=0)
            rate = form.number_input('Rate', min_value=0.00)

            calculate = form.form_submit_button('Calculate')

        if st.session_state.get('form_submit_button5') != True:
            st.session_state['form_submit_button5'] = calculate

        if st.session_state['form_submit_button5']:
            warning = ut.valid_input(rate,pv,None,None)
            if warning is not None:
                col2.warning(warning)
            else:
                fv = calculate_fv(expired, ['Bank'], [rate/100], [expired], pv, 0)
                result = pd.DataFrame(columns=['Bank'])
                result.loc[len(result.index)] = fv.iloc[-1:].values.tolist()[0]
                pmt = calculate_loan_pmt(
                    expired, ['Bank'], [rate/100], fv.iloc[-1:].values.tolist()[0])
                result.loc[len(result.index)] = pmt
                result = result.T.reset_index()
                result.columns = ['Bank', 'FV', 'PMT']
                col2.altair_chart(ut.generate_loan_chart(expired, result), use_container_width=True)
                mini_expander = st.expander('Detail')
                mini_expander.dataframe(result)