import streamlit as st
import pandas as pd
import numpy_financial as npf
import CrawlRateData as rd

deposit_rate = rd.get_deposit_rate()
loan_rate = rd.get_loan_rate()

def render_reference_saving():
    bank = st.selectbox("Choose The Bank", (deposit_rate['Bank']))
    reference_rate = get_reference_rate('Saving Rate', bank)

    fvtab, pvtab = st.tabs(["Expect Cash Flow", "Saving Goal"])
    with fvtab:
        form = st.form("fvform")
        duration = form.slider("Duration - Month", 1, 36)
        rate = get_rate('Saving Rate',reference_rate,duration)
        pv = form.number_input("Input Amount You Saving", step=100)
        pmt = form.number_input("Payment", step=100)
        submitted2 = form.form_submit_button(label="Submit")
        if (submitted2):
            string = "Deposit rate of {bank} in {duration} is: {rate}%"
            st.caption(string.format(
                bank=bank, duration=duration, rate=rate))
            rate = float(rate.replace(",", "."))/100/12
            expect_fv(rate=rate, duration=duration, pv=pv, pmt=pmt)

    with pvtab:
        form = st.form("pvform")
        duration = form.slider("Duration - Month", 1, 36)
        rate = get_rate('Saving Rate',reference_rate,duration)
        fv = form.number_input("Input Your Saving Goal", step=100)
        pmt = form.number_input("Payment", step=100)
        submitted2 = form.form_submit_button(label="Submit")
        if (submitted2):
            string = "Deposit rate of {bank} in {duration} is: {rate}%"
            st.caption(string.format(
                bank=bank, duration=duration, rate=rate))
            rate = float(rate.replace(",", "."))/100/12
            expect_pv(rate=rate, duration=duration, fv=fv, pmt=pmt)

def render_reference_loan():
    bank = st.selectbox("Choose The Bank", (loan_rate['Bank']))
    reference_rate = get_reference_rate('Loan Rate', bank)

def get_reference_rate(service, bank):
    st.header(service + " of " + bank)
    if (service == 'Saving Rate'):
        reference_rate = deposit_rate.loc[deposit_rate['Bank'] == bank]
    else:
        reference_rate = loan_rate.loc[loan_rate['Bank'] == bank]

    st.write(reference_rate.style.hide_index().to_html(),
             unsafe_allow_html=True)
    st.write("\n")
    return reference_rate


def get_rate(service, reference_rate, duration):
    rate = ""
    if(service == "Saving Rate"):
        duration_list = [int(str(col)[0:3]) for col in reference_rate.drop(
            'Bank', axis=1, inplace=False).columns]
        index = check_interval_value(duration_list, duration)
        while rate == "":
                rate = reference_rate.drop('Bank', axis=1).iat[0, index]
                index = index-1
                if index <= -1:
                    break

        if rate == "":
            st.warning("Bank not support")
    else:
        rate = reference_rate.iat[0,1]
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


def expect_fv(rate, duration, pv, pmt):
    result = npf.fv(rate=rate, nper=duration, pv=-pv, pmt=-pmt)
    st.markdown("Total cash that you will be received is:  <b style=\"color:green;\">{result}</b>".format(
        result="{:,}".format(result)), unsafe_allow_html=True)


def expect_pv(rate, duration, fv, pmt):
    result = npf.pv(rate=rate, nper=duration, fv=fv, pmt=-pmt)
    st.markdown("Total cash that you have to deposit from right now is: <b style=\"color:green;\">{result}</b>".format(
        result="{:,}".format(-result)), unsafe_allow_html=True)

