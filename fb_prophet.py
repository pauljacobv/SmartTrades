import streamlit as st
import matplotlib.pyplot as plt
from fbprophet import Prophet
import yfinance as yf
import datetime


class StockPredict:

    def __init__(self):
        self.model = Prophet(daily_seasonality=True)

    def data_statistics(self, data_stat):
        st.subheader('Data Statistics')
        st.write(data_stat.describe())

    @st.cache
    def get_stock_data(self, stockName):
        return yf.download(stockName)

    # @st.cache
    def get_prediction(self, df, start, end):
        data_range = df.loc[start:end]
        data_range = data_range.reset_index()
        data_pred = data_range[["Date", "Adj Close"]]  # select Date and Price
        data_pred = data_pred.rename(columns={"Date": "ds", "Adj Close": "y"})
        self.model.fit(data_pred)
        future = self.model.make_future_dataframe(periods=days_to_predict)
        return self.model.predict(future)


if __name__ == '__main__':

    st.title('Smart Trades')
    # data_load_state = st.text('Loading data...')
    st.sidebar.header('Enter Stock Name')
    stock_name = st.sidebar.text_input('Check Yahoo Finance for the exact listed name '
                                       'for eg. GOOG for Google', 'GOOG')

    sp = StockPredict()

    stockData = sp.get_stock_data(stockName=stock_name)
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
