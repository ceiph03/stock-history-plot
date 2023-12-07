import streamlit as st
import yfinance as yf
from datetime import date
import pandas as pd
import cufflinks as cf
import datetime

# App title
st.markdown('''
# Stock Price App
Shown are the stock price data for query companies!

**Credits**
- App built by [Chanin Nantasenamat](https://medium.com/@chanin.nantasenamat) (aka [Data Professor](http://youtube.com/dataprofessor))
- Built in `Python` using `streamlit`,`yfinance`, `cufflinks`, `pandas` and `datetime`
''')
st.write('---')

# Sidebar
st.sidebar.subheader('Query parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))

# Retrieving tickers data
ticker_list = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list) # Select ticker symbol
tickerData = yf.Ticker(tickerSymbol) # Get ticker data
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

# Ticker data
st.header('**Ticker data**')
st.write(tickerDf)

# Bollinger bands
st.header('**Bollinger Bands**')
qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')

# Create a layout with two columns
col1, col2 = st.columns([2, 1])

# Create a checkbox for toggling Bollinger Bands
bollinger_days = col1.selectbox('Period', [20,40,60,120])
add_bollinger_button = col2.button('Add Bollinger Bands')

# If the user wants to show Bollinger Bands, provide an input box for the number of days
if add_bollinger_button:
    # Add Bollinger Bands with the specified number of days
    qf.add_bollinger_bands(periods=bollinger_days)
    

fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)