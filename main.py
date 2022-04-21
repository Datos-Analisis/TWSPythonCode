from ib_insync import *
# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

stock = Forex('EURUSD')
#stock = Stock('SPY','SMART','USD')
bars = ib.reqHistoricalData(
    stock, endDateTime='', durationStr='30 D',
    barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

# convert to pandas dataframe:
df = util.df(bars)
#print(df)

def OnPendingTicker(ticker):
    print('pending ticker event recieved')
    print(ticker)


ib.pendingTickersEvent += OnPendingTicker

ib.run()