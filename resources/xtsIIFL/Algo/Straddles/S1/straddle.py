import configparser
import json
import os
from threading import Thread

from Ordsocket_client import OrderSocket_io
from facadeorder import XTconnect
from xtmarketdata import XTConnection
from msocket_client import MDSocket_io

global response, xt, ixt, mxt


class XTS:

    def __init__(self):

        pass

    def ex(self):
        """Redirect the user to the login url obtained from xt.login_url(), and receive the token"""

        currDirMain = os.getcwd()
        configParser = configparser.RawConfigParser()
        configFilePath = os.path.join(currDirMain, 'config.ini')
        configParser.read(configFilePath)
        self.port = configParser.get('socket', 'port').strip()

        self.isecretkey = configParser.get('USER', 'isecretkey').strip()
        self.msecretkey = configParser.get('USER', 'msecretkey').strip()
        self.interactiveKey = configParser.get('USER', 'iappKey').strip()
        self.marketDataKey = configParser.get('USER', 'mappKey').strip()
        self.source = configParser.get('USER', 'source').strip()
        self.port = configParser.get('socket', 'port').strip()

        print('------------------------------------------------------------------------')
        print("Interactive AppKey - " + self.interactiveKey)
        print("Interactive SecretKey - " + self.isecretkey)
        print("MarketData AppKey - " + self.marketDataKey)
        print("MarketData SecretKey - " + self.msecretkey)
        print("Source - " + self.source)
        print('------------------------------------------------------------------------')

        # Login
        ixt.login(self.isecretkey, self.interactiveKey, self.source)
        mxt.login(self.msecretkey, self.marketDataKey, self.source)

        # Set Token
        self.set_interactiveToken = ixt.set_token
        self.set_marketDataToken = mxt.set_token

        # Set UserID
        self.set_iuserID = ixt.userID
        self.set_muserID = mxt.userID

        #### SOCKET CONNECTION ####
        """Connected to the socket"""
        Thread(target=self.connectsocket).start()

        # Instruments for subscribing
        Instruments = [{'exchangeSegment': 1,
                        'exchangeInstrumentID': "NIFTY BANK"}]

        # mxt.sendSubscription(Instruments, 1504)
        self.getCESymbol()

    def connectsocket(self):
        soc = MDSocket_io(self.set_marketDataToken, self.set_muserID)
        el = soc.get_emitter()
        el.on('1504-json-full', self.on_message1504_json_full)
        socketconnect = soc.connect()

    def on_message1504_json_full(self, data):
        print('In main 1504 Index message!' + data)
        x = {}
        x = json.loads(data)
        indexValue = x["IndexValue"]
        print(x["IndexName"], " : ", x["IndexValue"])
        if x["IndexName"] == "NIFTY BANK":
            if x["IndexValue"] > 0:
                """Calculate ATM"""
                self.calculateATM(indexValue)

    def calculateATM(self, indexValue):
        atm = 0
        delta = int(indexValue%100)
        if delta > 50:
            atm = int((indexValue - delta) + 100) 
        else:
            atm = int(indexValue - delta)
        
        print("@@@@@ ATM @@@@@")
        print(atm)

    def getCESymbol(self):
        exchangeSegment=2,
        series='OPTIDX',
        symbol='NIFTY',
        expiryDate='24Jun2021',
        optionType='CE',
        strikePrice=15000
        a= mxt.getOptionSymbol(exchangeSegment, series, symbol, expiryDate, optionType, strikePrice)
        # a= mxt.getEquitySymbol(exchangeSegment,series, symbol)
        print(a)




if __name__ == "__main__":
    mxt = XTConnection()
    ixt = XTconnect()
    xts = XTS()
    xts.ex()
    Exit = input("Press Enter to Exit")
