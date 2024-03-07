import pandas as pd
import matplotlib.pyplot as plt

import yfinance as yf
from datetime import datetime
from prophet import Prophet
amzn = yf.Ticker("AMZN")

def forecast(start_date,forecast_period):
    end_date = datetime.now().strftime('%Y-%m-%d')
    #amzn_hist = amzn.history(start_date='2021-01-01',end=end_date)
    amzn_hist = amzn.history(start = start_date,end=end_date)

    # Reset index to make 'Date' a separate column
    df = amzn_hist.reset_index()

    df['Date'] = df['Date'].astype(str)

    df['Date'] = df['Date'].str[:-6]

    df['Date'] = pd.to_datetime(df['Date'])


    df = df[['Date', 'Close']]
    df = df.rename(columns={'Date': 'ds', 'Close': 'y'})

    m = Prophet()
    m.fit(df)

    #forecast_period = 100
    future = m.make_future_dataframe(periods=forecast_period)
    forecast = m.predict(future)

    forecast.tail()

    figure_1 = m.plot(forecast, xlabel='Date', ylabel='Price')

    #plt.axvline(x=forecast.iloc[-forecast_period]['ds'], c='r', linestyle='--')


    figure_2 = m.plot_components(forecast)
    #plt.show()
    
    return figure_1,figure_2

#fig = forecast('2021-01-01',100)


import streamlit as st

st.title("Forecasting App")

with st.form("my_form"):
    start_date = st.text_input("Start Date",value="2020-01-01",placeholder="yyyy-mm-dd", key="start_date_key")
    forecast_period = st.text_input("Forecast Period",value=100,placeholder="number",key="forecast_period_key")
    forecast_period = int(forecast_period)
    submitted = st.form_submit_button("Submit")
    
    
        
if submitted :
        #st.write("Submitted Succesfully",start_date,forecast_period)
        with st.spinner('Please wait...'):
            fig_1,fig_2 = forecast(start_date,forecast_period)
            st.pyplot(fig_1)
            st.pyplot(fig_2)


