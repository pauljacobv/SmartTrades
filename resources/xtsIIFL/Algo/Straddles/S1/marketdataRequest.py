import requests
import json
from requests.exceptions import HTTPError
from exception import *
import configparser
import os

global response, tokenn, userID
headers = {}
Instruments = []

currDirMain = os.getcwd()
configParser = configparser.RawConfigParser()
configFilePath = os.path.join(currDirMain, 'config.ini')
configParser.read(configFilePath)

port = configParser.get('socket', 'port').strip()
print("port", port)

prefix = configParser.get('marketdata_endpoints', 'prefix')


class Request_login:
    """
    :param  userID required to get the response from the server
    :param  password required to get the response from the server
    :param  publicKey required to get the response from the server
    :param  source required to get the response from the server
    
    """

    def login(self, secretKey, appKey, source):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'login')
            url = port + prefix + endpoint
            s = requests.Session()
            global tokenn, data, response, result, logs
            data = {'secretKey': secretKey, 'appKey': appKey, 'source': source}
            response = s.post(url, data=data, verify=False)
            print(response.text)
            result = response.text
            logs = json.loads(result)
            tokenn = logs['result']['token']
            self.set_token = tokenn
            self.userID=logs['result']['userID']
            return response.json()
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)



class Request_config:
    """
    :param  userID required to get the response from the server 
    :param  source required to get the response from the server 
    :param header is required for set Content-Type and authorization 
    """

    def get_config(self):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'clientconfig')
            url = port + prefix + endpoint
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            s = requests.Session()
            response = s.get(url, headers=headers, verify=False)
            print('Config :')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_quote:
    """
    :param  userID required to get the response from the server 
    :param  source required to get the response from the server
    :param clientID required for Uniquely identifies the user
    :param exchangeSegment required for which represents cash, derivative, commodity or currency market.
    :param exchangeInstrumentID required for Instrument Unique ID
    :param marketdataPort required to subscribe
    :param publishFormate required for publish to formate into Josn or binary
    :param header is required for set Content-Type and authorization
    """

    def get_quote(self, exchangeSegment, exchangeInstrumentID, exchangeSegment1,
                  exchangeInstrumentID1, xtsMessageCode, publishFormat):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'getquote')
            url = port + prefix + endpoint
            Instruments.append({'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID})
            Instruments.append({'exchangeSegment': exchangeSegment1, 'exchangeInstrumentID': exchangeInstrumentID1})
            s = requests.Session()
            qdata = {'instruments': Instruments, 'xtsMessageCode': xtsMessageCode, 'publishFormat': publishFormat}
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.post(url, data=json.dumps(qdata), headers=headers, verify=False)
            print('Quote :')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_subscribe:
    """
    :param  userID required to get the response from the server 
    :param  source required to get the response from the server
    :param clientID required for Uniquely identifies the user
    :param exchangeSegment required for which represents cash, derivative, commodity or currency market.
    :param exchangeInstrumentID required for Instrument Unique ID
    :param marketdataPort required to subscribe
    :param header is required for set Content-Type and authorization
    """

    def send_subscription(self, Instruments, xtsMessageCode):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'subscription')
            url = port + prefix + endpoint
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            sdata = {'instruments': Instruments, 'xtsMessageCode': xtsMessageCode}
            response = s.post(url, data=json.dumps(sdata), headers=headers, verify=False)

            print('Subscribe :')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_unsubscribe:
    """
    :param  userID required to get the response from the server 
    :param  source required to get the response from the server
    :param clientID required for Uniquely identifies the user
    :param exchangeSegment required for which represents cash, derivative, commodity or currency market.
    :param exchangeInstrumentID required for Instrument Unique ID
    :param marketdataPort required to subscribe
    :param header is required for set Content-Type and authorization
    """

    def send_unsubscription(self, exchangeSegment, exchangeInstrumentID, exchangeSegment1,
                            exchangeInstrumentID1, xtsMessageCode):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'unsubscribe')
            url = port + prefix + endpoint
            Instruments.append({'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID})
            Instruments.append({'exchangeSegment': exchangeSegment1, 'exchangeInstrumentID': exchangeInstrumentID1})
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            udata = {'instruments': Instruments, 'xtsMessageCode': xtsMessageCode}
            response = s.put(url, data=json.dumps(udata), headers=headers, verify=False)
            print('Unsubscribe :')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_master:
    """
    :param  userID required to get the response from the server
    :param  source required to get the response from the server
    :param clientID required for Uniquely identifies the user
    :param exchangeSegment required for which represents cash, derivative, commodity or currency market.
    :param exchangeInstrumentID required for Instrument Unique ID
    :param marketdataPort required to subscribe
    :param header is required for set Content-Type and authorization
    """

    def master(self, exchangeSegmentList):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'master')
            url = port + prefix + endpoint
            Instruments.append({'exchangeSegmentList': exchangeSegmentList})
            s = requests.Session()
            response = s.post(url, verify=False)
            print('Master :')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_OHLC:
    """
            :param exchangeSegment required for which represents cash, derivative, commodity or currency market.
            :param exchangeInstrumentID required for Instrument Unique ID
            :param startTime Standard date format or EPOCH Date
            :param endTime Standard date format or EPOCH Date
            :param compressionValue as In1Second:1 In1Minute: 60 InDaily : 86400
    """

    def getOHLC(self, exchangeSegment, exchangeInstrumentID, startTime, endTime, compressionValue):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'getohlc')
            url = port + prefix + endpoint + '?'
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            payload = {'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID,
                       'startTime': startTime, 'endTime': endTime, 'compressionValue': compressionValue}
            s = requests.Session()
            udata = {}
            response = s.get(url, params=payload, data=json.dumps(udata), headers=headers, verify=False)
            print('OHLC :')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_series:
    """
    :param  userID required to get the response from the server
    :param  source required to get the response from the server
    :param clientID required for Uniquely identifies the user
    :param exchangeSegment required for which represents cash, derivative, commodity or currency market.
    :param exchangeInstrumentID required for Instrument Unique ID
    :param marketdataPort required to subscribe
    :param header is required for set Content-Type and authorization
    """

    def getSeries(self, exchangeSegment):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'getseries')
            url = port + prefix + endpoint + '?'
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            payload = {'exchangeSegment': exchangeSegment}
            udata = {}
            response = s.get(url, params=payload, data=json.dumps(udata), headers=headers, verify=False)
            print('Series:')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_equity_symbol:
    """
    :param  exchangeSegment It is segment, which represents cash, derivative, commodity or currency market
    :param  series "EQ"
    :param  symbol "Acc"
    """

    def getEquitySymbol(self, exchangeSegment, series, symbol):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'getequitysymbol')
            url = port + prefix + endpoint + '?'
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            payload = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol}
            udata = {}
            response = s.get(url, params=payload, data=json.dumps(udata), headers=headers, verify=False)
            print('Equity Symbol:')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_expiry_date:
    """
    :param  exchangeSegment It is segment, which represents cash, derivative, commodity or currency market
    :param  series "EQ"
    :param  symbol "Acc"
    """

    def getExpiryDate(self, exchangeSegment, series, symbol):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'getexpirydate')
            url = port + prefix + endpoint + '?'
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            payload = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol}
            udata = {}
            response = s.get(url, params=payload, data=json.dumps(udata), headers=headers, verify=False)
            print('Expiry Date:')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_future_symbol:
    """
    :param  exchangeSegment It is segment, which represents cash, derivative, commodity or currency market
    :param  series "EQ"
    :param  symbol "Acc"
    :param  expiryDate "20Sep2019"
    """

    def getFutureSymbol(self, exchangeSegment, series, symbol, expiryDate):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'getfuturesymbol')
            url = port + prefix + endpoint + '?'
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            payload = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol, 'expiryDate': expiryDate}
            udata = {}
            response = s.get(url, params=payload, data=json.dumps(udata), headers=headers, verify=False)
            print('Future Symbol:')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_option_symbol:
    """
    :param  exchangeSegment It is segment, which represents cash, derivative, commodity or currency market
    :param  series "EQ"
    :param  symbol "Acc"
    :param  expiryDate "20Sep2019"
    """

    def getOptionSymbol(self, exchangeSegment, series, symbol, expiryDate, optionType, strikePrice):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'getoptionsymbol')
            url = port + prefix + endpoint + '?'
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            payload = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol, 'expiryDate': expiryDate,
                       'optionType': optionType, 'strikePrice': strikePrice}
            udata = {}
            response = s.get(url, params=payload, data=json.dumps(udata), headers=headers, verify=False)
            data = response.content.decode("utf8")
            return data
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_option_type:
    """
    :param  exchangeSegment It is segment, which represents cash, derivative, commodity or currency market
    :param  series "EQ"
    :param  symbol "Acc"
    :param  expiryDate "20Sep2019"
    """

    def getOptionType(self, exchangeSegment, series, symbol, expiryDate):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'getoptiontype')
            url = port + prefix + endpoint + '?'
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            payload = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol, 'expiryDate': expiryDate}
            udata = {}
            response = s.get(url, params=payload, data=json.dumps(udata), headers=headers, verify=False)
            print('Option Type:')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_index_list:
    """
    :param  exchangeSegment It is segment, which represents cash, derivative, commodity or currency market
    :param  series "EQ"
    :param  symbol "Acc"
    :param  expiryDate "20Sep2019"
    """

    def getIndexList(self, exchangeSegment):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'getindexlist')
            url = port + prefix + endpoint + '?'
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            payload = {'exchangeSegment': exchangeSegment}
            udata = {}
            response = s.get(url, params=payload, data=json.dumps(udata), headers=headers, verify=False)
            print('Index List:')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_search_instrumentID:
    """
    :param  userID required to get the response from the server 
    :param  source required to get the response from the server
    :param clientID required for Uniquely identifies the user
    :param exchangeSegment required for which represents cash, derivative, commodity or currency market.
    :param exchangeInstrumentID required for Instrument Unique ID
    :param header is required for set Content-Type and authorization
    """

    def search_by_instrumentid(self, source, isTradeSymbol, exchangeSegment, exchangeInstrumentID):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'searchbyinstrumentid')
            url = port + prefix + endpoint
            Instruments.append({'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID})
            s = requests.Session()
            udata = {'source': source, 'isTradeSymbol': isTradeSymbol, 'instruments': Instruments}
            response = s.post(url, data=json.dumps(udata), headers=headers, verify=False)
            print('Search By Instrument ID')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_searchString:
    """
    :param searchString required for search the insturment 
    :param header is required for set Content-Type and authorization
    """

    def search_by_Scriptname(self, searchString, source):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'searchbystring')
            url = port + prefix + endpoint
            payload = {'searchString': searchString, 'source': source}
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.get(url, headers=headers, verify=False, params=payload)
            print('Search By Symbol :')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Request_Logout:
    """:param  userID required to get the response from the server 
    :param  source required to get the response from the server
    :param header is required for set Content-Type and authorization

    """

    def logout(self):
        try:
            endpoint = configParser.get('marketdata_endpoints', 'logout')
            url = port + prefix + endpoint
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            s = requests.Session()
            response = s.delete(url, headers=headers, verify=False)
            print('Logout :')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)
