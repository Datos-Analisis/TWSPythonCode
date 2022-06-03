# Import libraries
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas as pd
import threading
import time
import csv
import datetime as dt

class TradeApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}

    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId] = [
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume}]
        else:
            self.data[reqId].append(
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume})
        print("reqID:{}, date:{}, open:{}, high:{}, low:{}, close:{}, volume:{}".format(reqId, bar.date, bar.open,
                                                                                        bar.high, bar.low, bar.close,
                                                                                        bar.volume))


def usTechStk(symbol, sec_type="STK", currency="USD", exchange="SMART"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract


def histData(req_num, contract, duration, candle_size):
    """extracts historical data"""
    app.reqHistoricalData(reqId=req_num,
                          contract=contract,
                          endDateTime='',
                          durationStr=duration,
                          barSizeSetting=candle_size,
                          whatToShow='TRADES',
                          useRTH=1,
                          formatDate=1,
                          keepUpToDate=0,
                          chartOptions=[])  # EClient function to request contract details


def websocket_con():
    app.run()


app = TradeApp()
app.connect(host='127.0.0.1', port=7497,
            clientId=23)  # port 4002 for ib gateway paper trading/7497 for TWS paper trading
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)  # some latency added to ensure that the connection is established

tickers = ["SPXU", "SPY"]
for ticker in tickers:
    histData(tickers.index(ticker), usTechStk(ticker), '2 D', '1 min')
    time.sleep(5)


###################storing trade app object in dataframe#######################
def dataDataframe(symbols, TradeApp_obj):
    "returns extracted historical data in dataframe format"
    df_data = {}
    for symbol in symbols:
        df_data[symbol] = pd.DataFrame(TradeApp_obj.data[symbols.index(symbol)],columns= ['Date','Open','High','Low','Close','Volume'])
        date_time = df_data[symbol]['Date']
        df_data[symbol]['Date'] = date_time.str.split(' ', expand=True)[0]
        df_data[symbol]['Hour'] = date_time.str.split(' ', expand=True)[2]
        df_data[symbol]['Hour'] = (pd.to_timedelta(df_data[symbol]['Hour'].astype(str))+pd.Timedelta(hours=1)).astype(str).str.split(' ', expand=True)[2]
        df_data[symbol]['Date'] = pd.to_datetime(df_data[symbol]['Date'], format='%Y%m%d').dt.strftime("%Y-%m-%d")
        df_data[symbol].set_index("Hour", inplace=True)
    return df_data


# extract and store historical data in dataframe
historical_data = dataDataframe(tickers, app)

####### Pasar a CSV

for ticker in tickers:
    historical_data[ticker].to_csv('{}.csv'.format(ticker),index=True, sep=',')

print(historical_data['SPXU'])