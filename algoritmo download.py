
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas as pd
import csv

class TestApp(EWrapper, EClient):

 def __init__(self):
  EClient.__init__(self, self)
  encabezado = ['Date','Hour', 'Open', 'Close', 'High', 'Low', 'Volume']
  self.df = pd.DataFrame(columns=encabezado)

 def error(self, reqId, errorCode, errorString):
  print("Error: ", reqId, " ", errorCode, " ", errorString)

 def historicalData(self, reqId, bar):
  print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,"Count:", bar.barCount, "WAP:", bar.average)
  hourNum = int(bar.date.split()[1][0:2])
  if hourNum == 23:
   hourNum= '00'
   hour = "".join([str(hourNum), bar.date.split()[1][2:8]])
  else:
   hourNum = hourNum+1
   hour = "".join([str(hourNum), bar.date.split()[1][2:8]])

  dftemp= pd.DataFrame({'Date': ["".join([bar.date.split()[0][0:4],'/',bar.date.split()[0][4:6],"/",bar.date.split()[0][6:8]])],'Hour':[hour],'Open': [bar.open],'Close': [bar.close], 'High': [bar.high], 'Low':[bar.low], 'Volume':[bar.volume]})
  self.df=pd.concat([self.df, dftemp],axis=0)
  self.df.to_csv('XLB.csv',index=False, sep=',')
  print(self.df)

def defineContract(symbol, secType, exchange,currency='USD'):
 contract = Contract()
 contract.symbol = symbol
 contract.secType = secType
 contract.exchange = exchange
 contract.currency = currency

 return contract

def main():
 app = TestApp()
 app.connect("127.0.0.1", 7497, 0)
 # define contract for EUR.USD forex pair
 contract = Contract()

 #contract.symbol = "EUR"
 #contract.secType = "CASH"
 #contract.exchange = "IDEALPRO"
 #contract.currency = "USD"

 contract.symbol = 'XLB'
 contract.secType = 'STK'
 contract.exchange = 'SMART'
 contract.currency = 'USD'
 contract.primaryExchange = 'NYSE'

 #app.reqHistoricalData(1, contract, "", "1 D", "1 min", "MIDPOINT", 0, 1, False,[])
 #app.reqHistoricalData(1, contract, "", "1 D", "1 min", "ADJUSTED_LAST", 1, 1, False,[])
 app.reqHistoricalData(1, contract, "", "6 D", "1 min", "TRADES", 1, 1, False, [])

 app.run()

if __name__ == "__main__":
 main()


