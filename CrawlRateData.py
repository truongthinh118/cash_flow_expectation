import json

import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup


@st.experimental_memo
def get_deposit_rate():
    r = requests.get("https://money24h.vn/lai-suat-gui-tiet-kiem-ngan-hang")
    soup = BeautifulSoup(r.text,'html.parser')
    div = soup.select("#__NEXT_DATA__")[0].text

    jsonObj = json.loads(div)["props"]["pageProps"]["savingRateAllBank"]

    for obj in jsonObj:
        label_rate = obj["results"]
        for rate in label_rate:
            label = rate["months"]
            rate =  rate["result"]
            try:
                rate =float(rate)
            except:
                rate = None
            obj[label] = rate
       
    df = pd.DataFrame(jsonObj).drop(['urlInterest', 'slug', 'share', 'results', 'linkBank','idPost','Không kỳ hạn'],axis=1)
    df = format_data(df)
    
    df.rename(columns= lambda col: col.replace("1 Tháng", " 1 Month").replace("Tháng", "Months"),inplace= True)
    return df

@st.experimental_memo
def get_loan_rate():
    r = requests.get("https://money24h.vn/lai-suat-vay-ngan-hang")
    soup = BeautifulSoup(r.text,'html.parser')
    div = soup.select("#__NEXT_DATA__")[0].text

    jsonObj = json.loads(div)["props"]["pageProps"]["loanRateAllBank"]

    for item in jsonObj:
        rate = item["results"]["result"]
        try:
            rate =float(rate)
        except:
            rate = None
        item["results"] = rate
    df = pd.DataFrame(jsonObj)[['bankName','results']]
    df = format_data(df)
    df.rename(columns= lambda col: col.replace("results","Rate"),inplace= True)
    return df

def format_data(data):
    df = pd.DataFrame(data).rename(columns= lambda col: col.replace("bankName", "Bank"))
    df = df.set_index('Bank').T.rename(columns=lambda col :col.replace("Ngân hàng ",""))
    df = df.T.sort_values(by=['Bank']).reset_index()
    float_columns = list(df.drop('Bank',axis=1,inplace=False).columns)
    # df[float_columns] = df[float_columns].applymap('{:.2f}'.format).astype(float)
    df[float_columns]= df[float_columns].round(decimals=2)
    df.index+=1
    return df
