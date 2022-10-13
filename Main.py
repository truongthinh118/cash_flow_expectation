from distutils.dep_util import newer_pairwise
from re import S
import streamlit as st
import numpy_financial as npf
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
    st.write("\n")
    duration = st.sidebar.selectbox("Duration",(duration_list))
    nper = int(str(duration)[1:3])
    rate = deposit_rate.loc[1][duration].replace(",",".")

    string = "Deposit rate of {bank} in {duration} is: {rate}%"
    st.caption(string.format(bank = bank, duration = duration, rate = rate))

    pv = st.sidebar.number_input("pv")
    pmt = st.sidebar.number_input("pmt")
    fv = st.sidebar.number_input("fv")
    st.write("You deposit {pv} to {bank} for {duration} with {rate}%:".format(pv=pv,bank=bank,duration=duration,rate=rate))

    rate = float(rate)/100/12
    
    if(pv==0 and fv ==0):
        st.warning("PV or FV must be greater than 0")
    elif (pv>0 and fv ==0):
        result = npf.fv(rate = rate, nper = nper , pv = -pv , pmt=-pmt)
        st.write("Total cash that you will be received is: {result}".format(result=result))
    elif(fv>0 and pv == 0):
        result = npf.pv(rate=rate,nper=nper,fv = fv,pmt =-pmt)
        st.write("Total cash that you have to deposit from right now is: {result}".format(result=result))
        

    

    


main()
