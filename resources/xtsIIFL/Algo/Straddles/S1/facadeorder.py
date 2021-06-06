from Xts_order import *
from Ordsocket_client import *
import requests
import json
from requests.exceptions import HTTPError
import configparser
import os


class XTconnect:
    def __init__(self):
        global log, prof, bal, plc, mo, tb, ob, po, co, pc, ex, sq, lout, oh, h, pcvrt, obc
        log = Request_login()
        prof = Profile()
        bal = Balance()
        plc = Place_Order()
        mo = Modify_order()
        tb = Tradebook()
        ob = OrderBook()
        oh = OrderHistory()
        po = Position()
        co = CancelOrder()
        pc = Place_cover()
        ex = Exitcover()
        sq = Squareoff()
        h = Holding()
        pcvrt = Position_convert()
        lout = Logout()
        obc = Getordstatus()

    def login(self, secretKey, appKey, source):
        self.log_in = log.login(secretKey, appKey, source)
        self.set_token = log.set_token
        self.isInvestorClient = log.isInvestorClient
        self.clientCodes = log.clientCodes
        self.userID = log.userID
        return self.log_in

    def getorderstatus(self, appOrderID):
        getord_status = obc.ord_status(appOrderID)
        return getord_status

    def getProfile(self, clientID):
        pr = prof.get_profile(clientID)
        return pr

    def getBalance(self):
        balance = bal.get_balance()
        return balance

    def placeOrder(self, exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, timeInForce,
                   disclosedQuantity, orderQuantity, limitPrice, stopPrice, orderUniqueIdentifier, clientID):
        pl = plc.place_order(exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, timeInForce,
                             disclosedQuantity, orderQuantity, limitPrice, stopPrice, orderUniqueIdentifier, clientID)
        return pl

    def modifyorder(self, appOrderID, modifiedProductType, modifiedOrderType, modifiedOrderQuantity,
                    modifiedDisclosedQuantity, modifiedLimitPrice, modifiedStopPrice, modifiedTimeInForce,
                    orderUniqueIdentifier, clientID):
        mod = mo.modify_order(appOrderID, modifiedProductType, modifiedOrderType, modifiedOrderQuantity,
                              modifiedDisclosedQuantity, modifiedLimitPrice, modifiedStopPrice, modifiedTimeInForce,
                              orderUniqueIdentifier, clientID)
        return mod

    def getOrderBook(self):
        OrderBook = ob.get_orderbook()
        return OrderBook

    def getTradebook(self, clientID):
        tbook = tb.get_trade(clientID)
        return tbook

    def getHolding(self, clientID):
        hdls = h.get_holding(clientID)
        return hdls

    def positionConvert(self, exchangeSegment, exchangeInstrumentID, targetQty, isDayWise, oldProductType, newProductType, clientID):
        pcv = pcvrt.position_Convert( exchangeSegment, exchangeInstrumentID, targetQty, isDayWise, oldProductType, newProductType, clientID)
        return pcv

    def getPosition(self, clientID):
        pday = po.get_Positionday(clientID)
        pnet = po.get_Positionnet(clientID)
        return pday, pnet

    def cancelorder(self, appOrderID, orderUniqueIdentifier,  clientID):
        cord = co.cancel_order(appOrderID, orderUniqueIdentifier, clientID)
        return cord

    def getOrderHistory(self, appOrderID, clientID):
        ordh = oh.get_orderhistory(appOrderID, clientID)
        return ordh

    def placeCoverOrder(self, exchangeSegment, exchangeInstrumentID, orderSide, orderQuantity, disclosedQuantity,
                        limitPrice, stopPrice, orderUniqueIdentifier, clientID):
        cod = pc.place_coverorder(exchangeSegment, exchangeInstrumentID, orderSide, orderQuantity, disclosedQuantity,
                                  limitPrice, stopPrice, orderUniqueIdentifier, clientID)
        return cod

    def exitcoverOrder(self, appOrderID, clientID):
        exc = ex.exitcover_order(appOrderID, clientID)
        return exc

    def squareoff(self, exchangeSegment, exchangeInstrumentID, productType, squareoffMode,
                  positionSquareOffQuantityType, squareOffQtyValue, blockOrderSending, cancelOrders, clientID):
        sqf = sq.squareoff(exchangeSegment, exchangeInstrumentID, productType, squareoffMode,
                           positionSquareOffQuantityType, squareOffQtyValue, blockOrderSending, cancelOrders, clientID)
        return sqf

    def logout(self):
        lo = lout.logout()
        return lo
