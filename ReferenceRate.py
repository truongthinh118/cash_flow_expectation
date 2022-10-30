from cgitb import reset
import streamlit as st
import pandas as pd
import altair as alt
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
        bank2 = col1.selectbox("", (bank_list), label_visibility='collapsed')
        selected_bank.append(bank2)
    reference_rate = get_reference_rate(service, selected_bank)

    fvtab, pvtab = st.tabs(["Expect Cash Flow", "Saving Goal"])
    with fvtab:
        form_process(service, selected_bank, reference_rate)


def render_reference_saving():
    render_refernce_page('Saving')


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
                "Period for Saving In "+bank+str(i+1), (period_list))
            periods.append(int(str(period)[0:3]))
            rate = get_rate(service, reference_rate, bank,
                            period_list.index(period))
            rates.append(float(rate.replace(",", "."))/100)
        pv = form.number_input("Input Amount You Saving", step=100)
    pmt = form.number_input("Payment", step=100)
    submitted2 = form.form_submit_button("Submit")
    if (submitted2):
        result = expect_fv(expire, selected_bank, rates, periods, pv, pmt)
        # result.index += 1

        line = alt.Chart(result.reset_index().melt('index')).mark_line(interpolate='step-after',point=True).encode(
            alt.X('index:Q', title="Months",scale=alt.Scale(domain=[0,expire], nice=False)),
            alt.Y('value', title='Value', scale=alt.Scale(zero=False)),
            color='variable'
        ).properties(
            height=400, width=650,
            title='Reference Saving Rate'
        ).configure_title(
            fontSize=16
        ).configure_axis(
            titleFontSize=14,
            labelFontSize=12
        )
        st.altair_chart(line)
        mini_expander = st.expander('Detail Cash Flow')
        mini_expander.dataframe(result)


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

    st.dataframe(reference_rate.style.hide_index())
    st.write("\n")
    return reference_rate


def get_rate(service, reference_rate, bank, period_index):
    rate = ""
    if (service == "Saving"):
        rate = reference_rate.set_index('Bank').T.iloc[period_index][bank]

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


def expect_fv(expire, banks, rates, periods, pv, pmt):
    df = pd.DataFrame()
    result = []
    if(banks.count(banks[0])>1):
        banks[0] = banks[0]+"_1"
        banks[1]= banks[1]+"_2"
    for i in range(len(banks)):
        bank = banks[i]
        period = periods[i]
        rate = rates[i]
        rate = rate * period / 12

        
        fv = []
        fv.append(pv)
        for j in range(expire+1):
            pre_fv = (fv[0]if j == 0 else fv[j-1])
            tem_fv = pre_fv
            if(j%period==0):
                tem_fv = (pre_fv * ((1 + rate)**j))+pmt
            if(j!=0):
                fv.append(tem_fv)
            
        result.append(fv)
    df = pd.DataFrame(result).T
    df.columns = banks
    return df


def expect_pv(rate, duration, fv, pmt):
    result = npf.pv(rate=rate, nper=duration, fv=fv, pmt=-pmt)
    st.markdown("Total cash that you have to deposit from right now is: <b style=\"color:green;\">{result}</b>".format(
        result="{:,}".format(-result)), unsafe_allow_html=True)
