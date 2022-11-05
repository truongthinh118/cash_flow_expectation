import numpy as np
import numpy_financial as npf
import pandas as pd
import streamlit as st

import CalculateFlow as cf
import CrawlRateData as rd
import Util as ut

reload_page = False


def render_reference_saving():
    selected_bank, reference_rate = render_refernce_page('Saving')
    
    fvtab, pmttab = st.tabs(["Expect Cash Flow", "Saving Goal"])

    with fvtab:
        col1, col2 = st.columns([4, 7])
        with col1:
            expired, result, banks, periods, rates, warning = form_process(
                'Saving', selected_bank, reference_rate, 'fv')
        if st.session_state['form_submit_button1']:
            if warning is not None:
                col2.warning(warning)
            else:
                col2.altair_chart(ut.generate_fv_chart(result, expired))
                mini_expander = st.expander('Detail Cash Flow') if len(selected_bank) <5 else col2.expander('Detail Cash Flow')
                for i in range(len(banks)):
                    mini_expander.write('Rate of '+banks[i]+' is: <b>'+str(
                        rates[i]*100)+'</b>% (compounding '+str(periods[i])+')', unsafe_allow_html=True)
                mini_expander.dataframe(result.T)

    with pmttab:
        col1, col2 = st.columns([4, 7])
        with col1:
            expired, result, banks, periods, rates, warning = form_process(
                'Saving', selected_bank, reference_rate, 'pmt')
        if st.session_state['form_submit_button2']:
            if warning is not None:
                col2.warning(warning)
            else:
                col2.altair_chart(ut.generate_pmt_chart(result))
                mini_expander = st.expander('Detail') if len(selected_bank) <5 else col2.expander('Detail')
                for i in range(len(banks)):
                    mini_expander.write('Rate of '+banks[i]+' is: <b>'+str(
                        rates[i]*100)+'</b>% (compounding '+str(periods[i])+')', unsafe_allow_html=True)
                mini_expander.dataframe(result)

def render_reference_loan():
    render_refernce_page("Loan")


def render_refernce_page(service):
    df = pd.DataFrame
    if (service == 'Saving'):
        df = rd.get_deposit_rate()
    else:
        df = rd.get_loan_rate()
    bank_list = list(df['Bank'])

    expander = st.expander('Reference '+service+' Rate Detail')
    ut.render_df(expander, df)

    col1, col2 = st.columns([6, 4])
    selected_bank = col1.multiselect(
        "Choose The Bank", bank_list, [bank_list[0]])
   
    reference_rate = get_reference_rate(service, df, selected_bank)
    return selected_bank, reference_rate


def form_process(service, selected_bank, reference_rate, key):
    form = st.form(key)
    result = pd.DataFrame()
    expired = form.number_input("Expired In - Months", step=1, min_value=1)
    banks = []
    periods = []
    rates = []
    pv = None
    fv = None
    pmt = None
    warning = None

    period_list = list(reference_rate.drop(
        'Bank', axis=1, inplace=False).columns)

    for i in range(len(selected_bank)):
        bank = selected_bank[i]
        period = form.selectbox(
            'Period for '+service+' In '+bank, (period_list), key=key+str(i))
        periods.append(period)

    for i in range(len(selected_bank)):
        bank = selected_bank[i]
        rate = get_rate(service, reference_rate, bank,
                        period_list.index(period))
        if not np.isnan(rate):
            rates.append(float(rate)/100)
            banks.append(bank)

    if key == 'pmt':
        fv = form.number_input("Input Your Saving Goal", step=100, min_value=0)

    pv = form.number_input("Input Amount You Have", step=100, min_value=0)

    if (key == 'fv'):
        pmt = form.number_input("Payment", step=100, min_value=0)
    
    submitted2 = form.form_submit_button("Submit")

    if key == 'fv':
        if st.session_state.get('form_submit_button1') != True:
            st.session_state['form_submit_button1'] = submitted2

        if st.session_state['form_submit_button1']:
            return fv_form(
                service, reference_rate, expired, banks,rates, period_list, periods, pv, fv, pmt)
    if key == 'pmt':
        if st.session_state.get('form_submit_button2') != True:
            st.session_state['form_submit_button2'] = submitted2

        if st.session_state['form_submit_button2']:
            return pmt_form(service, reference_rate, expired, banks,rates, period_list, periods, pv, fv, pmt)
    
    return expired, result, banks, periods, rates, warning

def fv_form(service, reference_rate, expired, banks,rates, period_list, periods, pv, fv, pmt):
    
    result = pd.DataFrame()
    
    warning = ut.valid_input(expired, banks, rates, periods, pv, fv, pmt)
    if warning is None:
        if len(banks) == 1:
            checkbox = st.checkbox(
                'Compare to other periods', value=False,key='fv')
            if checkbox:
                bank = banks[0]
                rates = []
                banks = []
                periods = []
                for period_item in period_list:
                    if int(str(period_item)[0:2])<=expired:
                        rate_item = get_rate(service, reference_rate, bank,
                                            period_list.index(period_item))
                        if not np.isnan(rate_item):
                            rates.append(float(rate_item)/100)
                            banks.append(bank)
                            periods.append(period_item)
        result = cf.expect_fv(expired, banks, rates, periods, pv, pmt)
    return expired, result, banks, periods, rates, warning

def pmt_form(service, reference_rate, expired, banks,rates, period_list, periods, pv, fv,pmt):
    result = []

    warning = ut.valid_input(expired, banks, rates, periods, pv, fv,None)
    if warning is None:
        if len(banks) == 1:
            checkbox = st.checkbox('Compare to other periods', value=False, key='pmt')
            if checkbox:
                bank = banks[0]
                rates = []
                banks = []
                periods = []
                for period_item in period_list:
                    if int(str(period_item)[0:2])<=expired:
                        rate_item = get_rate(service, reference_rate, bank,
                                            period_list.index(period_item))
                        if not np.isnan(rate_item):
                            rates.append(float(rate_item)/100)
                            banks.append(bank)
                            periods.append(period_item)
        result = cf.calculate_pmt(expired, banks, rates, periods, pv, fv)
    return expired, result, banks, periods, rates, warning

def get_reference_rate(service, df, selected_bank):
    st.header(service + " Rate of " + ", ".join(selected_bank))
    if (service == 'Saving'):
        reference_rate = df.loc[df['Bank'].isin(
            selected_bank)]
    else:
        reference_rate = df.loc[df['Bank'].isin(selected_bank)]

    col1, col2 = st.columns([6, 4])
    ut.render_df(col1, reference_rate)
    return reference_rate


def get_rate(service, reference_rate, bank, period_index):
    rate = ''
    if (service == 'Saving'):
        rate = reference_rate.set_index('Bank').T.iloc[period_index][bank]
    else:
        rate = reference_rate.iat[0, 1]
    # if (np.isnan(rate)):
    #     st.warning(bank + ' not support this period')
    return rate


# def check_interval_value(list, value):
#     mapping = []
#     for item in list:
#         mapping.append((item, list.index(item)))

#     for scale, output in mapping:
#         if value == scale:
#             return output
#         elif value < scale:
#             return output - 1


def expect_pv(rate, duration, fv, pmt):
    result = npf.pv(rate=rate, nper=duration, fv=fv, pmt=-pmt)
    st.markdown("Total cash that you have to deposit from right now is: <b style=\"color:green;\">{result}</b>".format(
        result="{:,}".format(-result)), unsafe_allow_html=True)
