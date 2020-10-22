import pandas as pd 

btc = pd.read_csv('Coinbase_BTCUSD_1h.csv')
eth = pd.read_csv('Coinbase_ETHUSD_1h.csv')
eth.info()
btc.info()
btc.columns
btc.reset_index(inplace=True)
eth.reset_index(inplace=True)

btc.columns= ['Unix_Timestamp', 'Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume_BTC', 'Volume_USD']
eth.columns= ['Unix_Timestamp', 'Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume_BTC', 'Volume_USD']

eth = eth.iloc[1:, :]
btc = btc.iloc[1:, :]
btc.head()
eth.head()
btc['Close'].astype(float).corr(eth['Close'].astype(float))
btc.Close
eth.Close.corr(btc.Close)

eth['Close'].astype(float).corr(btc['Close'].astype(float))
eth.iloc[-1, :]
btc.iloc[-1, :]


