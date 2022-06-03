from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

class TradingApp(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self,self)

    def error(self, reqId, errorCode, errorString):
        print("Error {} {} {}".format(reqId,errorCode, errorString))

    def contractDetails(self, reqId, contractDetails):
        print("reqID: {}, contract: {}".format(reqId,contractDetails))

    def historicalData(self, reqId, bar):
        print("HistoricalData. ReqID", reqId, "BarData.", bar)

def websocket_con():
    app.run()

app = TradingApp()
app.connect('127.0.0.1',7497, clientId=1)

con_thread = threading.Thread(target=websocket_con,daemon=True)
con_thread.start()
time.sleep(1)

contract = Contract()
contract.symbol = 'AAPL'
contract.secType = 'STK'
contract.currency = 'USD'
contract.exchange = 'NASDAQ'

app.reqHistoricalData(reqId=1,
                        contract=contract,
                        endDateTime='',
                        durationStr='3 M',
                        barSizeSetting='5 mins',
                        whatToShow='MIDPOINT',
                        useRTH=1,
                        formatDate=1,
                        keepUpToDate=0,
                        chartOptions=[])

time.sleep(5)
