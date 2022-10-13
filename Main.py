from re import S
import streamlit as st
import ta
from io import StringIO
import sys
import InterestRate

deposit_rate = InterestRate.get_deposit_rate()
bank_list = deposit_rate['Ngân hàng']
duration_list = deposit_rate.drop('Ngân hàng',axis=1,inplace=False).columns 

st.set_page_config(page_title ="Cash Flow Expection")
def main():
    st.title("Cash Flow Expection")
    st.sidebar.write("Choose the bank that you want to refer")
    bank = st.sidebar.selectbox("Bank",(bank_list))
    
    reference_rate = deposit_rate.loc[deposit_rate['Ngân hàng'] == bank]
    st.write(reference_rate.style.hide_index().to_html(),unsafe_allow_html=True)

    duration = st.selectbox("Duration",(duration_list))

    string = "You choose {bank} to refer the deposit cash flow in {duration}"
    st.caption(string.format(bank = bank, duration = duration))
    

    


main()
