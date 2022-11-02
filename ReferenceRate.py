import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import CrawlRateData as rd
import Util as ut

reload_page = False

def render_reference_saving():
    render_refernce_page('Saving')

def render_reference_loan():
    render_refernce_page("Loan")

def render_refernce_page(service):
    df = pd.DataFrame
    if (service == 'Saving'):
        df = rd.get_deposit_rate()
    else:
        df =  rd.get_loan_rate()
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
        bank2 = col1.selectbox("Bank", (bank_list), label_visibility='collapsed')
        selected_bank.append(bank2)
    reference_rate = get_reference_rate(service,df, selected_bank)

    fvtab, pvtab = st.tabs(["Expect Cash Flow", "Saving Goal"])
    with fvtab:
        form_process(service, selected_bank, reference_rate)


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
    supported_bank=[]
    for i in range(len(selected_bank)):
        bank = selected_bank[i]
        period = form.selectbox(
            'Period for '+service+' In '+bank, (period_list), key=i)
        periods.append(period)
        rate = get_rate(service, reference_rate, bank,
                        period_list.index(period))
        if not np.isnan(rate):
            rates.append(float(rate)/100)
            supported_bank.append(bank)
        
    pv = form.number_input("Input Amount You Saving", step=100,min_value=0)
    pmt = form.number_input("Payment", step=100,min_value=0)
    submitted2 = form.form_submit_button("Submit")
    if (submitted2):
        warning = ut.valid_input(expire, supported_bank, rates, periods, pv, fv, pmt)
        if warning is not None:
            st.warning(warning)
            
        else:
            result = expect_fv(expire, supported_bank, rates, periods, pv, pmt)
            # result.index += 1

            ut.render_chart(result,expire)
            mini_expander = st.expander('Detail Cash Flow')
            for i in range(len(supported_bank)):
                mini_expander.write('Rate of '+supported_bank[i]+' is: <b>'+str(rates[i]*100)+'</b>% (compunding '+str(periods[i])+')',unsafe_allow_html=True)
            mini_expander.dataframe(result.T)


def get_reference_rate(service,df, selected_bank):
    st.header(service + " Rate of " + ", ".join(selected_bank))
    if (service == 'Saving'):
        reference_rate = df.loc[df['Bank'].isin(
            selected_bank)]
    else:
        reference_rate = df.loc[df['Bank'].isin(selected_bank)]

    ut.render_df(st,reference_rate)
    return reference_rate

def get_rate(service, reference_rate, bank, period_index):
    rate = ''
    if (service == 'Saving'):
        rate = reference_rate.set_index('Bank').T.iloc[period_index][bank]
    else:
        rate = reference_rate.iat[0, 1]
    if (np.isnan(rate)):
        st.warning(bank + ' not support this period')
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
            tem_fv = fv[j-1] if (j % period != 0) else (pv * ((1 + rate)**(j//period)))+pmt
            fv.append(tem_fv)
            
        result.append(fv)
    df = pd.DataFrame(result).T
    df.columns = banks
    return df


def expect_pv(rate, duration, fv, pmt):
    result = npf.pv(rate=rate, nper=duration, fv=fv, pmt=-pmt)
    st.markdown("Total cash that you have to deposit from right now is: <b style=\"color:green;\">{result}</b>".format(
        result="{:,}".format(-result)), unsafe_allow_html=True)

