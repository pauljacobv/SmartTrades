import streamlit as st
import matplotlib.pyplot as plt
from prophet import Prophet
import yfinance as yf
import datetime
import numpy as np
import pandas as pd
from nsepy import get_history
from nsepy.derivatives import get_expiry_date
from nsepy import get_index_pe_history


class StockPredict:

    def __init__(self):
        self.model = Prophet(daily_seasonality=True)

    def data_statistics(self, data_stat):
        st.subheader('Data Statistics')
        st.write(data_stat.describe())

    # @st.cache
    def get_stock_data(self, stockName):
        return yf.download(stockName)

    def get_sliced_stockdata(self, df, start, end):
        return df.loc[start:end]
    # @st.cache
    def get_prediction(self, df, start, end):
        data_range = self.get_sliced_stockdata(df, start, end)
        data_range = data_range.reset_index()
        data_pred = data_range[["Date", "Adj Close"]]  # select Date and Price
        data_pred = data_pred.rename(columns={"Date": "ds", "Adj Close": "y"})
        self.model.fit(data_pred)
        future = self.model.make_future_dataframe(periods=days_to_predict)
        return self.model.predict(future)

    def call_payoff(self, sT, strike_price, premium):
        return np.where(sT > strike_price, sT - strike_price, 0) - premium

    def put_payoff(self, sT, strike_price, premium):
        return np.where(sT < strike_price, strike_price - sT, 0) - premium


if __name__ == '__main__':

    st.title('Smart Trades')
    # data_load_state = st.text('Loading data...')
    st.sidebar.header('Enter Stock Name')
    stock_name = st.sidebar.text_input('Check Yahoo Finance for the exact listed name '
                                       'for eg. ^NSEBANK for BANKNIFTY', 'INFY.NS')
    sp = StockPredict()

    stockData = sp.get_stock_data(stockName=stock_name)
    spot_price = stockData['Adj Close'][-1]

    st.write('Share price of ' + stock_name + ' is ' + str(spot_price))
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(stockData)

    today = datetime.date.today()
    one_year_back = today - datetime.timedelta(days=365)
    start_date = st.sidebar.date_input('Start date', one_year_back)
    end_date = st.sidebar.date_input('End date', today)

    if start_date > end_date:
        st.error('Error: End date must fall after start date.')

    days_to_predict = st.sidebar.number_input('Enter the number of days to predict', 1, 365)
    if st.checkbox('Show data stats between the date range'):
        sp.data_statistics(stockData.loc[start_date:end_date])

    if st.checkbox('Display predictions and trends'):
        prediction = sp.get_prediction(stockData, start_date, end_date)
        st.pyplot(sp.model.plot(prediction))
        plt.title("Prediction of the Google Stock Price using the Prophet")
        plt.xlabel("Date")
        plt.ylabel("Close Stock Price")
        st.pyplot(sp.model.plot_components(prediction))

    # Logarithmic Returns
    stockData['Log Returns'] = np.log(stockData['Adj Close']/stockData['Adj Close'].shift(1))
    # Computing Historical Volatility percentage
    volatility_window = st.sidebar.number_input('Enter the volatility window', 5, 365)
    stockData['Historical Volatility'] = 100*stockData['Log Returns'].rolling(window=volatility_window).std()
    HV_btw_start_end = sp.get_sliced_stockdata(stockData['Historical Volatility'], start_date, end_date)
    if st.checkbox('Display Historical Volatility'):
        st.line_chart(HV_btw_start_end)
        plt.title("Prediction of the Google Stock Price using the Prophet")
        plt.xlabel("Date")
        plt.ylabel("Close Stock Price")
        # st.pyplot(sp.model.plot_components(prediction))

    # Stock price range at expiration of the call
    sT = np.arange(0.95 * spot_price, 1.1 * spot_price, 1)
    if st.checkbox('Bull Call Spread'):
        col1, col2 = st.beta_columns(2)
        col1.header('Long call')
        col2.header('Short call')
        strike_price_long_call = col1.number_input('enter strike_price_long_call', 1380, 10000)
        strike_price_short_call = col2.number_input('enter strike_price_short_call', 1400, 10000)
        col11, col22 = st.beta_columns(2)
        premium_long_call = col11.number_input('enter premium for long call', 15, 100)
        premium_short_call = col22.number_input('enter premium for short call', 10, 100)
        payoff_long_call = sp.call_payoff(sT, strike_price_long_call, premium_long_call)
        payoff_short_call = sp.call_payoff(sT, strike_price_short_call, premium_short_call) * -1.0
        payoff_bull_call_spread = payoff_long_call + payoff_short_call
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.spines['bottom'].set_position('zero')
        ax.plot(sT, payoff_long_call, '--', label='Long Strike Call', color='g')
        ax.plot(sT, payoff_short_call, '--', label='Short Strike Call ', color='r')
        ax.plot(sT, payoff_bull_call_spread, label='Bull Call Spread')
        plt.xlabel('Infosys Stock Price')
        plt.ylabel('Profit and loss')
        plt.legend()
        plt.show()
        st.pyplot(fig)

    if st.checkbox('Bear Put Spread'):
        col1, col2 = st.beta_columns(2)
        col1.write('Long put')
        col2.write('Short put')
        strike_price_long_put = col1.number_input('enter strike_price_long_put', 1340, 10000)
        strike_price_short_put = col2.number_input('enter strike_price_short_put', 1300, 10000)
        col11, col22 = st.beta_columns(2)
        premium_long_put = col11.number_input('enter premium for long put', 15, 100)
        premium_short_put = col22.number_input('enter premium for short put', 10, 100)
        payoff_long_put = sp.put_payoff(sT, strike_price_long_put, premium_long_put)
        payoff_short_put = sp.put_payoff(sT, strike_price_short_put, premium_short_put) * -1.0
        payoff_bull_put_spread = payoff_long_put + payoff_short_put

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.spines['bottom'].set_position('zero')
        ax.plot(sT, payoff_long_put, '--', label='Long Strike put', color='g')
        ax.plot(sT, payoff_short_put, '--', label='Short Strike put ', color='r')
        ax.plot(sT, payoff_bull_put_spread, label='Bull Call Spread')
        plt.xlabel('Infosys Stock Price')
        plt.ylabel('Profit and loss')
        plt.legend()
        plt.show()
        st.pyplot(fig)

    if st.checkbox('Protective Put'):
        st.write('A protective put strategy is built by going long on a stock and simultaneously buying a put option.')
        col1, col2, col3 = st.beta_columns(3)
        col1.write('Stock purchase price')
        col2.write('Strike price long put')
        col3.write('Premium long put')
        stoke_price = col1.number_input('enter stock purchase price', spot_price, 10000.0)
        strike_price_long_put = col2.number_input('enter strike price short put', 1300.0, 10000.0)
        premium_long_put = col3.number_input('enter premium for long put', 5.0, 100.0)
        payoff_long_put = sp.put_payoff(sT, strike_price_long_put, premium_long_put)
        payoff_stock = sT - stoke_price
        payoff_protective_put = payoff_stock + payoff_long_put

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.spines['bottom'].set_position('zero')
        ax.plot(sT, payoff_stock, '--', label='Long Stock', color='g')
        ax.plot(sT, payoff_long_put, '--', label='Long Strike Put', color='r')
        ax.plot(sT, payoff_protective_put, label='Protective Put')
        plt.xlabel('Stock Price')
        plt.ylabel('Profit and loss')
        plt.legend()
        st.pyplot(fig)
    st.write('https://optioncreator.com/')
    print('done')