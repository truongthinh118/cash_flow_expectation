import streamlit as st
import pandas as pd
import numpy_financial as npf
import CrawlRateData as rd

deposit_rate = rd.get_deposit_rate()
loan_rate = rd.get_loan_rate()


def render_refernce_page(service):
    df = pd.DataFrame
    if (service == 'Saving'):
        df = deposit_rate
    else:
        df = loan_rate
    bank_list = (df['Bank'])

    expander = st.expander('Reference '+service+' Rate Detail')
    render_expander(expander, df)

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
        bank2 = col1.selectbox("", (bank_list.drop(
            df.loc[bank_list == bank].index, axis=0, inplace=False)), label_visibility='collapsed')
        selected_bank.append(bank2)
    reference_rate = get_reference_rate(service, selected_bank)

    fvtab, pvtab = st.tabs(["Expect Cash Flow", "Saving Goal"])
    with fvtab:
        form_process(service, selected_bank, reference_rate)


def render_reference_saving():
    render_refernce_page('Saving')
    # bank_list = (deposit_rate['Bank'])
    # expander = st.expander('Reference Saving Rate Detail')
    # render_expander(expander)
    # col1,col2 = st.columns(2)
    # bank = col1.selectbox("Choose The Bank", (bank_list))
    # selected_bank=[bank]
    # col2.write("\n")
    # col2.write("\n")
    # # onclick = col2.button("+")
    # container = col2.container().empty()

    # if st.session_state.get('button1') != True:
    #     st.session_state['button1'] = container.button("+")

    # if st.session_state['button1']:
    #     container.empty()
    #     bank2 = col1.selectbox("",(bank_list.drop(deposit_rate.loc[bank_list==bank].index,axis=0,inplace=False)),label_visibility='collapsed')
    #     selected_bank.append(bank2)
    # reference_rate = get_reference_rate('Saving Rate', selected_bank)

    # fvtab, pvtab = st.tabs(["Expect Cash Flow", "Saving Goal"])
    # with fvtab:
    #     form = st.form("fvform")
    #     duration = form.slider("Duration - Month", 1, 36)
    #     rate = get_rate('Saving Rate',reference_rate,duration)
    #     pv = form.number_input("Input Amount You Saving", step=100)
    #     pmt = form.number_input("Payment", step=100)
    #     submitted2 = form.form_submit_button(label="Submit")
    #     if (submitted2):
    #         string = "Deposit rate of {bank} in {duration} is: {rate}%"
    #         st.caption(string.format(
    #             bank=bank, duration=duration, rate=rate))
    #         rate = float(rate.replace(",", "."))/100/12
    #         expect_fv(rate=rate, duration=duration, pv=pv, pmt=pmt)

    # with pvtab:
    #     form = st.form("pvform")
    #     duration = form.slider("Duration - Month", 1, 36)
    #     rate = get_rate('Saving Rate',reference_rate,duration)
    #     fv = form.number_input("Input Your Saving Goal", step=100)
    #     pmt = form.number_input("Payment", step=100)
    #     submitted2 = form.form_submit_button(label="Submit")
    #     if (submitted2):
    #         string = "Deposit rate of {bank} in {duration} is: {rate}%"
    #         st.caption(string.format(
    #             bank=bank, duration=duration, rate=rate))
    #         rate = float(rate.replace(",", "."))/100/12
    #         expect_pv(rate=rate, duration=duration, fv=fv, pmt=pmt)


def render_expander(expander, df):
    expander.dataframe(df)
    expander.write("\n")


def form_process(service, selected_bank, reference_rate):
    form = st.form("form")
    expire = form.number_input("Expire In (Month)", step=1)

    periods = []
    rates = []
    pv = 0
    fv = 0
    pmt = 0

    if service == 'Saving':
        period_list = list(reference_rate.drop(
            'Bank', axis=1, inplace=False).columns)
        for i in range(len(selected_bank)):
            bank = selected_bank[i]
            period = form.selectbox(
                "Period for Saving In "+bank, (period_list))
            periods.append(int(str(period)[0:3]))
            rate = get_rate(service, reference_rate, bank,
                            period_list.index(period))
            rates.append(rate)
        pv = form.number_input("Input Amount You Saving", step=100)
    pmt = form.number_input("Payment", step=100)
    submitted2 = form.form_submit_button("Submit")
    if (submitted2):
        expect_fv(expire,selected_bank,rates,periods,pv,pmt)
        # for i in range(len(selected_bank)):
        #     rate = rates[i]
        #     rate = float(rate.replace(",", "."))/100/12
        #     period = int(str(periods[i])[0:3])
        #     if(True):
        #         expect_fv(rate=rate, duration=expire,period=period, pv=pv, pmt=pmt)


def render_reference_loan():
    # bank = st.selectbox("Choose The Bank", (loan_rate['Bank']))
    # reference_rate = get_reference_rate('Loan Rate', bank)
    render_refernce_page("Loan")


def get_reference_rate(service, selected_bank):
    st.header(service + " Rate of " + ", ".join(selected_bank))
    if (service == 'Saving'):
        reference_rate = deposit_rate.loc[deposit_rate['Bank'].isin(
            selected_bank)]
    else:
        reference_rate = loan_rate.loc[loan_rate['Bank'].isin(selected_bank)]

    st.write(reference_rate.style.hide_index().to_html(),
             unsafe_allow_html=True)
    st.write("\n")
    return reference_rate


def get_rate(service, reference_rate, bank, period_index):
    rate = ""
    if (service == "Saving"):
        rate = reference_rate.set_index('Bank').T.iloc[period_index][bank]
        # duration_list = [int(str(col)[0:3]) for col in reference_rate.drop(
        #     'Bank', axis=1, inplace=False).columns]
        # index = check_interval_value(duration_list, duration)
        # while rate == "":
        #         rate = reference_rate.drop('Bank', axis=1).iat[0, index]
        #         index = index-1
        #         if index <= -1:
        #             break

    else:
        rate = reference_rate.iat[0, 1]
    return rate


def check_interval_value(list, value):
    mapping = []
    for item in list:
        mapping.append((item, list.index(item)))

    for scale, output in mapping:
        if value == scale:
            return output
        elif value < scale:
            return output - 1


def expect_fv(expire,banks,rates,periods,pv,pmt):
    # result = npf.fv(rate=rate, nper=duration, pv=-pv, pmt=-pmt)
    # st.markdown("Total cash that you will be received is:  <b style=\"color:green;\">{result}</b>".format(
    #     result="{:,}".format(result)), unsafe_allow_html=True)
    df = pd.DataFrame
    for i in range(len(banks)):
        bank = bank[i]
        rate = rates[i]
        period = periods[i]

        cycle_time = expire//period
        # for j in range(1,cycle_time):
            



    


    


def expect_pv(rate, duration, fv, pmt):
    result = npf.pv(rate=rate, nper=duration, fv=fv, pmt=-pmt)
    st.markdown("Total cash that you have to deposit from right now is: <b style=\"color:green;\">{result}</b>".format(
        result="{:,}".format(-result)), unsafe_allow_html=True)
