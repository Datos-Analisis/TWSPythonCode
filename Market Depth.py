from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.contract import *
from ibapi.ticktype import *
import datetime
import threading
import time
import datetime
import pandas as pd

RUN_FLAG = False


class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)


class TestWrapper(EWrapper):
    def __init__(self):
        EWrapper.__init__(self)

    def updateMktDepth(self, reqId: TickerId, position: int, operation: int, side: int, price: float, size: int):
        global df
        super().updateMktDepth(reqId, position, operation, side, price, size)
        print("UpdateMarketDepth", "ReqId:", reqId, "Position:", position, "Operation:", operation, "Side:", side,
              "Price:", price, "Size:", size)

        time = datetime.datetime.now()
        cols = ['Time', 'ReqId', 'Position', 'Operation', 'Side', 'Price', 'Size']
        data = [time, reqId, position, operation, side, price, size]
        csv_file = 'C:/Users/Workstation 4/PycharmProjects/TWSPythonCode/Depth.csv'

        d2 = pd.DataFrame(data, cols)
        d2 = d2.T
        df = df.append(d2)
        df.to_csv(csv_file)

        print(df)

    def updateMktDepthL2(self, reqId: TickerId, position: int, marketMaker: str,
                         operation: int, side: int, price: float, size: int, isSmartDepth: bool):
        super().updateMktDepthL2(reqId, position, marketMaker, operation, side,
                                 price, size, isSmartDepth)
        print("UpdateMarketDepthL2", "ReqId:", reqId, "Position:", position, "MarketMaker:", marketMaker, "Operation:",
              operation, "Side:", side, "Price:", price, "Size:", size, "isSmartDepth:", isSmartDepth)

    def error(self, reqId: TickerId, errorcode: int, errorString: str):
        print("Error= ", reqId, " ", errorcode, " ", errorString)

    def contratDetails(self, reqId: int, contractDetails: ContractDetails):
        print("ContractDetails: ", reqId, " ", contractDetails)

    def historicalData(self, reqId: int, bar: BarData):
        print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open,
              "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
              "Count:", bar.barCount, "WAP:", bar.average)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        global RUN_FLAG
        print("HistoricalDataEnd ", reqId, "from", start, "to", end)
        RUN_FLAG = False

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ", reqId, " Date:", bar.date, "Open:", bar.open,
              "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
              "Count:", bar.barCount, "WAP:", bar.average)

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("TickPrice. TickerId:", reqId, "tickType:", tickType,
              "Price:", price, "CanAutoExecute:", attrib.canAutoExecute,
              "PastLimit:", attrib.pastLimit, end=' ')
        if tickType == TickTypeEnum.BID or tickType == TickTypeEnum.ASK:
            print("PreOpen:", attrib.preOpen)
        else:
            print()

    def connectAck(self):
        global RUN_FLAG
        print("Connect ACK")
        RUN_FLAG = True

    def nextValidId(self, orderId: int):
        self.nextOrderId = orderId
        print("I have nextValidId", orderId)


def main():
    data = []  # Attempting to append to list
    try:
        while True:
            global RUN_FLAG
            wrapper = TestWrapper()
            client = TestClient(wrapper)
            client.connect("127.0.0.1", 7496, 101)
            print("Done with connect()")

            t = threading.Thread(name="TWSAPI_worker", target=client.run)
            t.start()
            print("Returned from run()")

            while not RUN_FLAG:
                time.sleep(1)
                print("No orders")

            contract = Contract()
            contract.symbol = 'SPY'
            contract.secType = 'STK'
            contract.exchange = 'SMART'
            contract.currency = 'USD'
            contract.primaryExchange = 'NYSE'

            client.reqMktDepth(1, contract, 20, False, [])  # tried data.append(....)


            print("Returned from call to reqHistoricalData()")
            print("Waiting to finish.")

            while RUN_FLAG:
                time.sleep(1)
                print("No orders")

    except KeyboardInterrupt:
        print("ALL DONE!")
        print(data)  # data list remains blank
        client.disconnect()


if __name__ == "__main__":
    main()