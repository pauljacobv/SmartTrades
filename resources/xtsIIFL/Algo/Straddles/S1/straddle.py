import os
import json
import time
import schedule
import datetime
import requests
import configparser
from threading import Thread
from facadeorder import XTconnect
from xtmarketdata import XTConnection
from msocket_client import MDSocket_io
from Ordsocket_client import OrderSocket_io

global response, xt, ixt, mxt
ceFlag = True
peFlag = True
ceSLMFlag = False
peSLMFlag = False


class XTS:

    def __init__(self):

        pass

    def ex(self):
        """Redirect the user to the login url obtained from xt.login_url(), and receive the token"""

        currDirMain     = os.getcwd()
        configParser    = configparser.RawConfigParser()
        configFilePath  = os.path.join(currDirMain, 'config.ini')

        configParser.read(configFilePath)

        self.port           = configParser.get('socket', 'port').strip()
        self.isecretkey     = configParser.get('USER', 'isecretkey').strip()
        self.msecretkey     = configParser.get('USER', 'msecretkey').strip()
        self.interactiveKey = configParser.get('USER', 'iappKey').strip()
        self.marketDataKey  = configParser.get('USER', 'mappKey').strip()
        self.source         = configParser.get('USER', 'source').strip()
        self.port           = configParser.get('socket', 'port').strip()

        self.telegramtoken  = configParser.get('Telegram', 'token').strip()
        self.telegramchatid = configParser.get('Telegram', 'chatid').strip()

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

        # Set Client ID
        self.client_List = ixt.clientCodes
        self.clientID = self.client_List[0]

        #### SOCKET CONNECTION ####
        """Connected to the socket"""
        Thread(target=self.connectsocket).start()

        # Instruments for subscribing
        Instruments = [{
            'exchangeSegment': 1,
            'exchangeInstrumentID': "NIFTY BANK"
        }]

        mxt.sendSubscription(Instruments, 1504)
        
    def connectsocket(self):
        soc = MDSocket_io(self.set_marketDataToken, self.set_muserID)
        el = soc.get_emitter()
        el.on('1504-json-full', self.on_message1504_json_full)
        socketconnect = soc.connect()

    def on_message1504_json_full(self, data):
        # print('In main 1504 Index message!' + data)
        x = {}
        x = json.loads(data)
        indexValue = x["IndexValue"]
        print(x["IndexName"], " : ", x["IndexValue"])
        if x["IndexName"] == "NIFTY BANK":
            if x["IndexValue"] > 0:
                """Calculate ATM"""
                self.getStrikePrice(indexValue)

    def getStrikePrice(self, indexValue):
        strikePrice = 0
        delta = int(indexValue % 100)
        if delta > 50:
            strikePrice = int((indexValue - delta) + 100)
        else:
            strikePrice = int(indexValue - delta)

        print("ATM Value :" + str(strikePrice))

        self.getCESymbol(strikePrice)
        self.getPESymbol(strikePrice)

    def getCESymbol(self, strikePrice):
        exchangeSegment = 2
        series = 'OPTIDX'
        symbol = 'BANKNIFTY'
        expiryDate = self.next_weekday(datetime.date.today(), 3)
        optionType = 'CE'
        strikePrice = strikePrice
        ce = mxt.getOptionSymbol(
            exchangeSegment, series, symbol, expiryDate, optionType, strikePrice)
        ce = json.loads(ce)
        ceSymbol = ce["result"][0]["Description"]
        print("CE Symbol :"+ str(ceSymbol))
        if(str(strikePrice) in ceSymbol):
            if(ceFlag):
                # BANKNIFTY2161035400CE
                po_CE = self.placeorder(
                    "NSEFO",
                    int(ce["result"][0]["ExchangeInstrumentID"]),
                    "MIS",
                    "MARKET",
                    "SELL",
                    75,
                    0,
                    0,
                    datetime.datetime.now().strftime("ST%d%m%Y%H%M%S")
                )

                print("### CE ORDER RESPONSE ###")
                print(po_CE)
                print("-------------------------")
                self.checkOrderStatus("CE", po_CE["result"]["AppOrderID"])
        else:
            print("ERROR IN CE SYMBOL")

    def getPESymbol(self, strikePrice):
        exchangeSegment = 2
        series = 'OPTIDX'
        symbol = 'BANKNIFTY'
        expiryDate = self.next_weekday(datetime.date.today(), 3)
        optionType = 'PE'
        strikePrice = strikePrice
        pe = mxt.getOptionSymbol(
            exchangeSegment, series, symbol, expiryDate, optionType, strikePrice)
        pe = json.loads(pe)
        peSymbol = pe["result"][0]["Description"]
        print("PE Symbol :"+ str(peSymbol))
        if(str(strikePrice) in peSymbol):
            if(peFlag):
                # BANKNIFTY2161035400PE
                po_PE = self.placeorder(
                    "NSEFO",
                    int(pe["result"][0]["ExchangeInstrumentID"]),
                    "MIS",
                    "MARKET",
                    "SELL",
                    75,
                    0,
                    0,
                    datetime.datetime.now().strftime("ST%d%m%Y%H%M%S")
                )

                print("### PE ORDER RESPONSE ###")
                print(po_PE)
                print("-------------------------")
                self.checkOrderStatus("PE", po_PE["result"]["AppOrderID"])
        else:
            print("ERROR IN PE SYMBOL")

    def placeorder(self, exchangesegment, instrumentid, producttype, ordertype, orderside, orderQuantity, limitPrice, stopPrice, orderUniqueIdentifier):
        response_data = ixt.placeOrder(
            exchangesegment,
            instrumentid,
            producttype,
            ordertype,
            orderside,
            "DAY",
            0,
            orderQuantity,
            limitPrice,
            stopPrice,
            orderUniqueIdentifier,
            self.clientID
        )
        return response_data

    def placeSLM(self, TradingSymbol, ExchangeInstrumentID, OrderAverageTradedPrice):
        
        if(TradingSymbol == "CE" and not ceSLMFlag):
            CE_SLM_Price = float(OrderAverageTradedPrice.strip() or 0) + 50
            po_CESLM = self.placeorder(
                    "NSEFO",
                    int(ExchangeInstrumentID),
                    "MIS",
                    "StopMarket",
                    "BUY",
                    75,
                    0,
                    CE_SLM_Price,
                    datetime.datetime.now().strftime("CESLM%d%m%Y%H%M%S")
                )

            print("### CE SLM ORDER RESPONSE ###")
            print(po_CESLM)
            print("-------------------------")
            self.checkOrderStatus("CESLM", po_CESLM["result"]["AppOrderID"])

        elif(TradingSymbol == "PE" and not peSLMFlag):
            PE_SLM_Price = float(OrderAverageTradedPrice.strip() or 0) + 60
            po_PESLM = self.placeorder(
                    "NSEFO",
                    int(ExchangeInstrumentID),
                    "MIS",
                    "StopMarket",
                    "BUY",
                    75,
                    0,
                    PE_SLM_Price,
                    datetime.datetime.now().strftime("PESLM%d%m%Y%H%M%S")
                )

            print("### PE SLM ORDER RESPONSE ###")
            print(po_PESLM)
            print("-------------------------")
            self.checkOrderStatus("PESLM", po_PESLM["result"]["AppOrderID"])

    def checkOrderStatus(self, TradingSymbol, AppOrderID):

        global ceFlag, peFlag, ceSLMFlag, peSLMFlag

        response_data = ixt.getorderstatus(
            AppOrderID
        )

        for results in response_data['result']:

            if(results['OrderStatus'] == "Filled"):

                if(TradingSymbol == "CE"):
                    ceFlag = False
                    self.placeSLM(TradingSymbol, results['ExchangeInstrumentID'], results['OrderAverageTradedPrice'])
                if(TradingSymbol == "PE"):
                    peFlag = False
                    self.placeSLM(TradingSymbol, results['ExchangeInstrumentID'], results['OrderAverageTradedPrice'])
                if(TradingSymbol == "CESLM"):
                    ceSLMFlag = True
                    print("Send Telegram Message CESLM")
                if(TradingSymbol == "PESLM"):
                    peSLMFlag = True
                    print("Send Telegram Message PESLM")
                    

            elif(results['OrderStatus'] == "Rejected"):
                print("Order Rejected")
                print("Send Telegram Message - Order Rejected - TradingSymbol")

    def next_weekday(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return (d + datetime.timedelta(days_ahead)).strftime('%d%b%Y')

    def telegram_bot_sendtext(self, bot_message):

        bot_token   = self.telegramtoken
        bot_chatID  = self.chatID
        send_text   = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        
        response = requests.get(send_text)
    
        return response.json()

if __name__ == "__main__":
    mxt = XTConnection()
    ixt = XTconnect()
    xts = XTS()
    xts.ex()
    # schedule.every().day.at("09:30").do(xts.ex)
    while True:
        schedule.run_pending()
        time.sleep(1)