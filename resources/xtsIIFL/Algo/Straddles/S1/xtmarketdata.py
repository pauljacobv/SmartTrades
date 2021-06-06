from marketdataRequest import *
import requests
import json
from requests.exceptions import HTTPError
global tokkenn


class XTConnection:
	def __init__(self):
		global mlog, prof, qut, subsc, unsubc, searchid, searchS, lout, mast, ohlc, series, eqsym, exdate, fusym, opsym, optyp, il
		mlog = Request_login()
		prof = Request_config()
		qut = Request_quote()
		subsc = Request_subscribe()
		unsubc = Request_unsubscribe()
		searchid = Request_search_instrumentID()
		searchS = Request_searchString()
		lout = Request_Logout()
		mast = Request_master()
		ohlc = Request_OHLC()
		series = Request_series()
		eqsym = Request_equity_symbol()
		exdate = Request_expiry_date()
		fusym = Request_future_symbol()
		opsym = Request_option_symbol()
		optyp = Request_option_type()
		il = Request_index_list()

	# AUTH Section =============================================================================================

	def login(self, secretKey, appKey, source):
		logg_in = mlog.login(secretKey, appKey, source)
		self.set_token=mlog.set_token
		self.userID=mlog.userID
		return logg_in

	def logout(self):
		logg_out = lout.logout()
		return logg_out

	# Client Config Section =============================================================================================

	def getConfig(self):
		confg = prof.get_config()
		return confg

	# Instruments Section =============================================================================================

	def getQuote(self, exchangeSegment, exchangeInstrumentID, exchangeSegment1, exchangeInstrumentID1, xtsMessageCode, publishFormat):
		gt_qt = qut.get_quote(exchangeSegment, exchangeInstrumentID, exchangeSegment1, exchangeInstrumentID1, xtsMessageCode, publishFormat)
		return gt_qt

	def sendSubscription(self, Instruments, xtsMessageCode):
		subb = subsc.send_subscription(Instruments, xtsMessageCode)
		return subb 

	def sendUnsubscription(self, exchangeSegment, exchangeInstrumentID, exchangeSegment1, exchangeInstrumentID1, xtsMessageCode):
		unsub = unsubc.send_unsubscription(exchangeSegment, exchangeInstrumentID, exchangeSegment1, exchangeInstrumentID1, xtsMessageCode)
		print(unsub)

	def master(self, exchangeSegmentList):
		mas = mast.master(exchangeSegmentList)
		return mas

	def getSeries(self, exchangeSegment):
		ser = series.getSeries(exchangeSegment)
		return ser

	def getEquitySymbol(self, exchangeSegment, series, symbol):
		sym = eqsym.getEquitySymbol(exchangeSegment, series, symbol)
		return sym

	def getExpiryDate(self, exchangeSegment, series, symbol):
		exp = exdate.getExpiryDate(exchangeSegment, series, symbol)
		return exp

	def getFutureSymbol(self, exchangeSegment, series, symbol, expiryDate):
		fus = fusym.getFutureSymbol(exchangeSegment, series, symbol, expiryDate)
		return fus

	def getOptionSymbol(self, exchangeSegment, series, symbol, expiryDate, optionType, strikePrice):
		ops = opsym.getOptionSymbol(exchangeSegment, series, symbol, expiryDate, optionType, strikePrice)
		return ops

	def getOptionType(self, exchangeSegment, series, symbol, expiryDate):
		opt = optyp.getOptionType(exchangeSegment, series, symbol, expiryDate)
		return opt

	def getIndexList(self, exchangeSegment):
		index = il.getIndexList(exchangeSegment)
		return index

	# OHLC Section =============================================================================================

	def getOHLC(self, exchangeSegment, exchangeInstrumentID, StartDate, EndDate, compressionType):
		mas = ohlc.getOHLC(exchangeSegment, exchangeInstrumentID, StartDate, EndDate, compressionType)
		return mas

	# Search Section =============================================================================================

	def search_by_instrumentid(self, source, isTradeSymbol, exchangeSegment, exchangeInstrumentID):
		sr_instr = searchid.search_by_instrumentid(source, isTradeSymbol, exchangeSegment, exchangeInstrumentID)
		print(sr_instr)

	def search_by_Scriptname(self, searchString, source):
		sr_scrpt = searchS.search_by_Scriptname(searchString, source)
		print(sr_scrpt)





