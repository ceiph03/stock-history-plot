import pandas as pd
import yfinance as yf
from datetime import datetime
import seaborn as sns
from matplotlib import pyplot as plt
sns.set(font_scale=1.0)


class Stock:

    def __init__(self, ticker, start, end):
        self.ticker = ticker
        df = yf.download(ticker, start=start, end=end)
        df = pd.DataFrame(df)
        df['Date'] = df.index
        self.df = df

    # freq: ex.. every 'Y', 'M', 'W', 'D', fund is the total invest amount
    def invest(self, freq, fund=1):
        self.df = self.df.resample(freq).first().dropna()
        self.df.set_index('Date', inplace=True)
        self.df['Date'] = self.df.index
        self.df['invest'] = fund / self.df.count()[0]
        self.df['cum_invest'] = self.df['invest'].cumsum()
        self.df['nETF'] = self.df['invest'] / self.df['Adj Close']
        self.df['price change (%)'] = (
            self.df['Adj Close'] - self.df['Adj Close'].iloc[0]) / self.df['Adj Close'].iloc[0] * 100
        self.df['cum_nETF'] = self.df['nETF'].cumsum()
        self.df['cum_return (USD)'] = self.df['cum_nETF'] * \
            self.df['Adj Close']
        self.df['cum_ROI (%)'] = (self.df['cum_return (USD)'] -
                                  self.df['cum_invest']) / self.df['cum_invest'] * 100
        self.freq = freq

        return self

    @staticmethod
    def plot(objs):
        fig, ax = plt.subplots(3, 1, figsize=(8, 6), dpi=150)
        ax[0].set_ylabel('ROI [%]')
        ax[1].set_ylabel('Price change [%]')

        for obj in objs:
            sns.lineplot(data=obj.df, x='Date', y='cum_ROI (%)',
                         label=f'{obj.ticker} by {obj.freq}', ax=ax[0])
            sns.lineplot(data=obj.df, x='Date', y='price change (%)',
                         label=f'{obj.ticker} by {obj.freq}', ax=ax[1])

        ax[0].legend(loc='upper left', bbox_to_anchor=(1, 1))
        ax[1].get_legend().remove()
        plt.tight_layout()

        # Create the table using the DataFrame
        df = pd.concat([x.df.iloc[-1][['cum_ROI (%)', 'price change (%)']]
                       for x in objs], axis=1)
        df = df.astype('float32')
        df.columns = [x.ticker for x in objs]
        sns.heatmap(data=df, annot=True, fmt=f".0f",
                    annot_kws={'size': 12, 'fontweight': 'bold'},
                    cmap='coolwarm', ax=ax[-1])

        plt.tight_layout()

        return fig, ax, df
