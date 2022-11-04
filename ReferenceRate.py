import numpy as np
import numpy_financial as npf
import pandas as pd
import streamlit as st

import CalculateFlow as cf
import CrawlRateData as rd
import Util as ut

reload_page = False


def render_reference_saving():
    selected_bank, reference_rate= render_refernce_page('Saving')
    fvtab, pvtab = st.tabs(["Expect Cash Flow", "Saving Goal"])
    with fvtab:
        form_process('Saving', selected_bank, reference_rate)



def render_reference_loan():
    render_refernce_page("Loan")


def render_refernce_page(service):
    df = pd.DataFrame
    if (service == 'Saving'):
        df = rd.get_deposit_rate()
    else:
        df = rd.get_loan_rate()
    bank_list = (df['Bank'])

    expander = st.expander('Reference '+service+' Rate Detail')
    ut.render_df(expander, df)

    col1, col2 = st.columns(2)
    bank = col1.selectbox("Choose The Bank", (bank_list))
    selected_bank = [bank]
    col2.write("\n")
    col2.write("\n")
    # onclick = col2.button("+")
    container = col2.container().empty()

    if st.session_state.get('button1') != True:
        st.session_state['button1'] = container.button("+")

    if st.session_state['button1']:
        container.empty()
        bank2 = col1.selectbox("Bank", (bank_list),
                               label_visibility='collapsed')
        selected_bank.append(bank2)
    reference_rate = get_reference_rate(service, df, selected_bank)
    return selected_bank, reference_rate

    

def form_process(service, selected_bank, reference_rate):
    form = st.form("form")
    expire = form.number_input("Expire In (Month)", step=1, min_value=1)

    periods = []
    rates = []
    pv = None
    fv = None
    pmt = None

    period_list = list(reference_rate.drop(
        'Bank', axis=1, inplace=False).columns)

    for i in range(len(selected_bank)):
        bank = selected_bank[i]
        period = form.selectbox(
            'Period for '+service+' In '+bank, (period_list), key=i)
        periods.append(period)

    pv = form.number_input("Input Amount You Saving", step=100, min_value=0)
    pmt = form.number_input("Payment", step=100, min_value=0)
    submitted2 = form.form_submit_button("Submit")

    if st.session_state.get('form_submit_button') != True:
        st.session_state['form_submit_button'] = submitted2

    if st.session_state['form_submit_button']:
        banks = []
        for i in range(len(selected_bank)):
            bank = selected_bank[i]
            rate = get_rate(service, reference_rate, bank,
                            period_list.index(period))
            if not np.isnan(rate):
                rates.append(float(rate)/100)
                banks.append(bank)

        warning = ut.valid_input(expire, banks, rates, periods, pv, fv, pmt)
        if warning is not None:
            st.warning(warning)
        else:
            # result = expect_fv(expire, banks, rates, periods, pv, pmt)
            # result.index += 1
            if not st.session_state['button1']:
                checkbox = st.checkbox(
                    'Compare to other periods', value=False, key='compare')
                if checkbox:
                    bank = banks[0]
                    rates = []
                    banks = []
                    periods = []
                    for period_item in period_list:
                        rate_item = get_rate(service, reference_rate, bank,
                                             period_list.index(period_item))
                        if not np.isnan(rate_item):
                            rates.append(float(rate_item)/100)
                            banks.append(bank)
                            periods.append(period_item)
            result = cf.expect_fv(expire, banks, rates, periods, pv, pmt)

            ut.render_chart(result, expire)

            mini_expander = st.expander('Detail Cash Flow')
            for i in range(len(banks)):
                mini_expander.write('Rate of '+banks[i]+' is: <b>'+str(
                    rates[i]*100)+'</b>% (compounding '+str(periods[i])+')', unsafe_allow_html=True)
            mini_expander.dataframe(result.T)


def get_reference_rate(service, df, selected_bank):
    st.header(service + " Rate of " + ", ".join(selected_bank))
    if (service == 'Saving'):
        reference_rate = df.loc[df['Bank'].isin(
            selected_bank)]
    else:
        reference_rate = df.loc[df['Bank'].isin(selected_bank)]

    ut.render_df(st, reference_rate)
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
