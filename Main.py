import streamlit as st
import numpy_financial as npf
import InterestRate

deposit_rate = InterestRate.get_deposit_rate()
bank_list = deposit_rate['Bank']
duration_list =[int(str(col)[0:3]) for col in deposit_rate.drop('Bank',axis=1,inplace=False).columns]

st.set_page_config(page_title ="Cash Flow Expectation",page_icon="💲",initial_sidebar_state="expanded")
def main():
    st.title("Cash Flow Expectation")
    st.sidebar.write("Choose The Service And The Bank You Want To Refer")

    service = st.sidebar.selectbox("Service",(["Deposit","Loan"]))
    bank = st.sidebar.selectbox("Bank",(bank_list))
           
    submitted = st.sidebar.button(label="Submit",key="side_button")

    if st.session_state.get('button1') != True:
        st.session_state['button1'] = submitted


    if st.session_state['button1']:
        reference_rate = render_reference_rate(service,bank)
        fvtab,pvtab = st.tabs(["FV","PV"])
    
        with fvtab:
            form = st.form("fvform")
            duration = form.slider("Duration - month",1,36)
            index = check_interval_value(duration_list,duration)
            rate = reference_rate.drop('Bank',axis=1).iat[0,index]
            pv = form.number_input("PV",step = 100)
            pmt = form.number_input("PMT",step = 100)
            submitted2 = form.form_submit_button(label = "Submit")
            if(submitted2):
                while rate == "":
                    index = index-1
                    rate = reference_rate.drop('Bank',axis=1).iat[0,index]

                string = "Deposit rate of {bank} in {duration} is: {rate}%"
                st.caption(string.format(bank = bank, duration = duration, rate = rate))
                rate = float(rate.replace(",","."))/100/12
                expect_fv(rate=rate,duration=duration,pv=pv,pmt=pmt)
                
        with pvtab:
            form = st.form("pvform")
            duration = form.slider("Duration - month",1,36)
            index = check_interval_value(duration_list,duration)
            rate = reference_rate.drop('Bank',axis=1).iat[0,index]
            fv = form.number_input("FV",step = 100)
            pmt = form.number_input("PMT",step = 100)
            submitted2 = form.form_submit_button(label = "Submit")
            if(submitted2):
                while rate == "":
                    index = index-1
                    rate = reference_rate.drop('Bank',axis=1).iat[0,index]

                string = "Deposit rate of {bank} in {duration} is: {rate}%"
                st.caption(string.format(bank = bank, duration = duration, rate = rate))
                rate = float(rate.replace(",","."))/100/12
                expect_pv(rate=rate,duration=duration,fv=fv,pmt=pmt)
    
def check_interval_value(list, value):
    mapping = []
    for item in list:
        mapping.append((item,list.index(item)))
    
    for scale, output in mapping:
        if value == scale:
            return output
        elif value < scale:
            return output - 1
    
def render_reference_rate(service,bank):
    st.header(service + " rate of "+ bank)
    reference_rate = deposit_rate.loc[deposit_rate['Bank'] == bank]
    st.write(reference_rate.style.hide_index().to_html(),unsafe_allow_html=True)
    st.write("\n")
    return reference_rate

def expect_fv(rate,duration,pv,pmt):
    result = npf.fv(rate = rate, nper = duration , pv = -pv , pmt=-pmt)
    st.write("Total cash that you will be received is:  <b style=\"color:green;\">{result}</b>".format(result=result),unsafe_allow_html=True)
    
def expect_pv(rate,duration,fv,pmt):
    result = npf.pv(rate=rate,nper=duration,fv = fv,pmt =-pmt)
    st.markdown("Total cash that you have to deposit from right now is: <b style=\"color:green;\">{result}</b>".format(result=result),unsafe_allow_html=True)


main()
