# stock history plot
You can plot and calculate ROI based on historical data of tickers.
You have to save `finance.py` in the same folder where your `main.py` is located in.

`Please find stock.ipynb for an example (same as below)`

```
import finance
import pandas as pd
import yfinance as yf
from datetime import datetime
import seaborn as sns
from matplotlib import pyplot as plt
sns.set(font_scale=1.0)

freq = 'W' #'M' -monthly investment, 'W' - weekly investment
start = datetime(2018,6,16) # Define starting day
end = datetime(2023,6,16) #Define ending day
instances = []
tickers = ['btc-usd','spy','qqq','aapl','goog','amzn','tsla','nvda','tsm']
#Provide ticker names you want to plot and calculate ROI.
for ticker in tickers:
    instance = Stock(ticker,start,end).invest(freq)
    instances.append(instance)
Stock.plot(instances)
```

![image](https://github.com/ceiph03/stock-history-plot/assets/35480900/00c2e984-e1fa-4e7b-98c6-52fcdab89f6d)
