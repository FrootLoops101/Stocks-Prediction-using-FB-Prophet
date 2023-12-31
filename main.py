import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

from prophet import Prophet
from prophet.plot import plot_plotly

import pandas_datareader
import datetime
import yfinance as yf

import pandas_datareader.data as web

# Define start and end dates
start = datetime.datetime(2018, 1, 1)
end = datetime.datetime(2023, 1, 1)

# Download stock data using yfinance
tesla = yf.download('TSLA', start, end)
amazon = yf.download('AMZN', start, end)
google = yf.download('GOOGL', start, end)


# Define a function to plot stock data
def plot_stock_data(df, symbol):
    df['Open'].plot(label=symbol, title='Open Price')
    plt.legend()


# Plot stock data for each company
plot_stock_data(tesla, 'TESLA')
plot_stock_data(amazon, 'AMAZON')
plot_stock_data(google, 'GOOGLE')
plt.show()


# Define a function to prepare stock data for Prophet model
def prepare_stock_data(df):
    hist_data = df[['Close']]
    hist_data.reset_index(level=0, inplace=True)
    hist_data = hist_data.rename({'Date': 'ds', 'Close': 'y'}, axis='columns')
    return hist_data


# Prepare stock data for each company
hist_tesla = prepare_stock_data(tesla)
hist_amazon = prepare_stock_data(amazon)
hist_google = prepare_stock_data(google)


# Define a function to fit and forecast with Prophet model
def fit_forecast_prophet(hist_data, symbol):
    m = Prophet(daily_seasonality=True)
    m.fit(hist_data)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    pd.options.display.max_columns = None
    print(forecast.tail(2))

    figure1 = m.plot(forecast)
    ax = figure1.gca()
    ax.set_title(f"Forecasted Stock Prices of {symbol}", size=30)
    ax.set_xlabel("Time", size=30)
    ax.set_ylabel("Stock Prices", size=30)
    figure2 = m.plot_components(forecast)


# Fit and forecast with Prophet model for each company
fit_forecast_prophet(hist_tesla, 'TESLA')
fit_forecast_prophet(hist_amazon, 'AMAZON')
fit_forecast_prophet(hist_google, 'GOOGLE')
