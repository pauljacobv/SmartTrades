import configparser
import json
import os
from threading import Thread

from Ordsocket_client import OrderSocket_io
from facadeorder import XTconnect
from xtmarketdata import XTConnection
from msocket_client import MDSocket_io

global response, xt,ixt,mxt


class Example:

    def __init__(self):
        
        pass

    def ex(self):
        """Redirect the user to the login url obtained from xt.login_url(), and receive the token"""

        

        currDirMain = os.getcwd()
        configParser = configparser.RawConfigParser()
        configFilePath = os.path.join(currDirMain, 'config.ini')
        configParser.read(configFilePath)
        self.port = configParser.get('socket', 'port').strip()

        #self.userID = configParser.get('USER', 'userID').strip()
        self.isecretkey = configParser.get('USER', 'isecretkey').strip()
        self.msecretkey = configParser.get('USER', 'msecretkey').strip()
        self.interactiveKey = configParser.get('USER', 'iappKey').strip()
        self.marketDataKey = configParser.get('USER', 'mappKey').strip()
        self.source = configParser.get('USER', 'source').strip()
        self.port = configParser.get('socket', 'port').strip()

        print('------------------------------------------------------------------------')
        #print("User ID - " + self.userID)
        print("Interactive SecretKey - " + self.isecretkey)
        print("Interactive AppKey - " + self.interactiveKey)
        print("MarketData SecretKey - " + self.msecretkey)
        print("MarketData AppKey - " + self.marketDataKey)
        print("Source - " + self.source)
        print('------------------------------------------------------------------------')

        # marketdata
        mxt.login(self.msecretkey, self.marketDataKey, self.source)

        # interactive
        ixt.login(self.isecretkey, self.interactiveKey, self.source)
        self.set_interactiveToken = ixt.set_token
        self.set_marketDataToken = mxt.set_token
        self.set_iuserID=ixt.userID
        self.set_muserID=mxt.userID
        # self.isInvestorClient = ixt.isInvestorClient
        # self.isInvestorClient = mxt.isInvestorClient

        # self.client_List = ixt.clientCodes

        ############################
        soc = MDSocket_io(self.set_marketDataToken, self.set_muserID)
        """Connected to the socket"""
        Thread(target=self.connectsocket).start()
        """Connected to the socket"""
        ordsoc = OrderSocket_io(self.set_interactiveToken,self.set_iuserID)
        Thread(target=self.connectinteractve_socket).start()

        # Instruments = [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
        #                {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]

        Instruments = [{'exchangeSegment': 1, 'exchangeInstrumentID': "NIFTY BANK"}]


        mxt.sendSubscription(Instruments, 1504)
        # mxt.sendSubscription(Instruments, 1501)

        """Place the order"""
        self.set_interactiveToken = ixt.set_token
        self.isInvestorClient = ixt.isInvestorClient
        self.client_List = ixt.clientCodes
        self.clientID = self.client_List[0]

    def placeorder(self, exchangesegment, instrumentid, producttype,ordertype, orderside, orderQuantity, price):
        response_data = ixt.placeOrder(exchangesegment, instrumentid, producttype, ordertype, orderside, "DAY",
                                      price,orderQuantity, 0, 0, "test_0001",
                                      self.clientID)

    def on_message1501_json_full(self, data):
        print('in main 1501 Level1,Touchline message!' + data)
        # tick = {}
        tick = json.loads(data)

        if tick['ExchangeInstrumentID'] == 2885:
            touchline = {}
            touchline = tick.get("Touchline")
            if touchline is not None and touchline.get('LastTradedPrice') > 1200:
                """Call Place Order For Instrument needed"""
                print("@@@@@@PRICEE " + str(touchline.get("LastTradedPrice")))
                self.placeorder("NSECM", 2885, "NRML", "MARKET", "BUY",1, 0.0)

    def on_message1504_json_full(self, data):
        print('in main 1504 Index message!'+ data)
        x = {}
        x = json.loads(data)
        print(x["IndexName"], " : ", x["IndexValue"])
        if x["IndexName"] == "NIFTY BANK":
            if x["IndexValue"] < 0:
                """Call Place Order For Instrument needed"""
                self.placeorder()

    def on_orders(self, data):
        print('Orders!!!' + data)

    def on_trades(self, data):
        print('trades!!!' + data)

    def on_position(self, data):
        print('Position!!!' + data)

    def connectsocket(self):
        soc = MDSocket_io(self.set_marketDataToken, self.set_muserID)
        el = soc.get_emitter()
        # el.on('1501-json-full', self.on_message1501_json_full)
        el.on('1504-json-full', self.on_message1504_json_full)
        socketconnect = soc.connect()

    def connectinteractve_socket(self):
        ordsoc = OrderSocket_io(self.set_interactiveToken,self.set_iuserID)
        i1 = ordsoc.get_emitter()
        i1.on('order', self.on_orders)
        i1.on('trade', self.on_trades)
        i1.on('position', self.on_position)
        ordsocketconnect = ordsoc.connect()


if __name__ == "__main__":
    mxt = XTConnection()
    ixt = XTconnect()
    c1 = Example()
    c1.ex()
    Exit = input("Press Enter to Exit")
