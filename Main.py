from re import S
import streamlit as st
import ta
from io import StringIO
import sys
import InterestRate

deposit_rate = InterestRate.get_deposit_rate()
bank_list = deposit_rate['Bank']
duration_list = deposit_rate.drop('Bank',axis=1,inplace=False).columns 

st.set_page_config(page_title ="Cash Flow Expection")
def main():
    st.title("Cash Flow Expection")

    st.sidebar.write("Choose the service of bank you want to refer")

    service = st.sidebar.selectbox("Service",(["Deposit","Loan"]))
    bank = st.sidebar.selectbox("Bank",(bank_list))
    
    st.header(service + " rate of "+ bank)
    reference_rate = deposit_rate.loc[deposit_rate['Bank'] == bank]
    st.write(reference_rate.style.hide_index().to_html(),unsafe_allow_html=True)

    duration = st.selectbox("Duration",(duration_list))

    rate = deposit_rate.loc[1][duration]

    string = "Deposit rate of {bank} in {duration} is: {rate}%"
    st.caption(string.format(bank = bank, duration = duration, rate = rate))

    

    


main()
