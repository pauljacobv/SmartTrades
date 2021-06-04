import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
import json
from exception import ExceptionHandle
import configparser
import os
import ssl
import certifi
import urllib3


global response, tokenn, port, prefix, userID, client_List, session
data = {}
currDirMain = os.getcwd()
configParser = configparser.RawConfigParser()
configFilePath = os.path.join(currDirMain, 'config.ini')
configParser.read(configFilePath)
port = configParser.get('socket', 'port').strip()
end_point = configParser.get('interactive_endpoints', 'login')
prefix = configParser.get('interactive_endpoints', 'prefix')

headers = {}


class Request_login:
    """
    :param  userID required to get the response from the server
    :param  secretKey required to get the response from the server
    :param  appKey required to get the response from the server
    :param  source required to get the response from the server
    
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    xts_adapter = HTTPAdapter(max_retries=3)
    session = requests.Session()
    session.mount(port, xts_adapter)

    def login(self, secretKey, appKey, source):
        try:
            url = port + prefix + end_point
            xts_adapter = HTTPAdapter(max_retries=3)
            session = requests.Session()
            session.mount(port, xts_adapter)
            s = session

            global tokenn, isInvestorClient, clientID, client_List
            data = {'secretKey': secretKey, 'appKey': appKey, 'source': source}
            response = s.post(url, data=data, verify=False)

            datajson = response.json()
            print("RESPONSE:----------------------------\n" + str(datajson))
            tokenn = datajson['result']['token']

            isInvestorClient = datajson['result']['isInvestorClient']
            clientCodes = datajson['result']['clientCodes']
            self.userID=datajson['result']['userID']
            print("USERID:------------------------------\n" + datajson['result']['userID'])
            print("\nInvestorClient = " + str(isInvestorClient))
            print("\nClient Code = " + str(clientCodes))

            self.set_token = tokenn
            self.isInvestorClient = isInvestorClient
            self.clientCodes = clientCodes
            return response.json()
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Getordstatus():

    def ord_status(self, appOrderID):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            if not isInvestorClient:
                headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
                end_point = '/orders'
                url = port + prefix + end_point

            else:
                end_point = '/orders?appOrderID={}'.format(appOrderID)
                url = port + prefix + end_point

            get_orderbook_data = {}
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.get(url, data=json.dumps(get_orderbook_data), headers=headers, verify=False)
            print(f'\nOrder Book:{response.json()}')

            return response.json()
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Place_Order:
    """
        :param exchangeSegment required for which represents cash, derivative, commodity or currency market.
        :param exchangeInstrumentID required for Instrument Unique ID.
        :param productType required for identify the category of the order like CNC,NRML,MIS etc.
        :param orderType is Market or limit.
        :param timeInForce is required to indicate how long order will remain active.
        :param disclosedQuantity is an order in which only a part of the order quantity is disclosed to the market
        :param orderQuantity is the number of Sell or Buy orders
        :param limitPrice is a price used during a limit order when buying a security
        :param stopPrice is the price in a stop order that triggers the creation of a market order.
        :param orderUniqueIdentifier is user specific Order Unique Identifier 
        :param header is required for set Content-Type and authorization
    
        """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def place_order(self, exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, timeInForce,
                    disclosedQuantity, orderQuantity, limitPrice, stopPrice, orderUniqueIdentifier, clientID):
        try:
            global response
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            end_point = configParser.get('interactive_endpoints', 'placeorder')

            place_data = {'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID,
                          'productType': productType, 'orderType': orderType, 'orderSide': orderSide,
                          'timeInForce': timeInForce, 'disclosedQuantity': disclosedQuantity,
                          'orderQuantity': orderQuantity, 'limitPrice': limitPrice, 'stopPrice': stopPrice,
                          'orderUniqueIdentifier': orderUniqueIdentifier
                          }

            if not isInvestorClient:
                place_data['clientID'] = clientID
            else:
                pass

            url = port + prefix + end_point
            xts_adapter = HTTPAdapter(max_retries=3)
            session = requests.Session()
            session.mount(port, xts_adapter)
            s = requests.Session()
            response = s.post(url, data=json.dumps(place_data), headers=headers, verify=False)
            response_data = response.json()

            print(f'\nPlace order: {response.json()}')

            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)

        return response_data


class Profile():
    """Required for accessing User Profile access  """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_profile(self, clientID):
        try:
            endpoint = configParser.get('interactive_endpoints', 'getprofile')
            params={}
            if not isInvestorClient:
                params = {'clientID': clientID}
            else:
                pass
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            s = requests.Session()
            url = port + prefix + endpoint
            response = s.get(url, params=params, headers=headers, verify=False)
            print(f'\nProfile : {response.json()}')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Balance():
    """Required for accessing balance details related limit on equityrelated to limits on equities, derivative,
    upfront margin etc """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_balance(self):
        if isInvestorClient == True:
            try:
                end_point = configParser.get('interactive_endpoints', 'getbalance')
                url = port + prefix + end_point
                s = requests.Session()
                balance_data = {}
                headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
                response = s.get(url, data=json.dumps(balance_data), headers=headers, verify=False)
                print(f'\nBalance :{response.json()}')
                raise ExceptionHandle
            except ExceptionHandle:
                ExceptionHandle.checkResponse(response)
        else:
            print(
                "Balance :\nBalance API available for retail API users only, dealers can watch the same on dealer terminal")


class Modify_order():
    """:param exchangeSegment required for which represents cash, derivative, commodity or currency market.
        :param appOrderID required for modify the order .
        :param modifiedproductType required for modified the category of the order like CNC,NRML,MIS etc.
        :param modifiedorderType is Market or limit.
        :param modifiedtimeInForce is required to indicate how long order will remain active.
        :param modifieddisclosedQuantity is an order in which only a part of the order quantity is disclosed to the market
        :param modifiedorderQuantity is the number of Sell or Buy orders
        :param modifiedlimitPrice is a price used during a limit order when buying a security
        :param modifiedstopPrice is the price in a stop order that triggers the creation of a market order.
        :param orderUniqueIdentifier is user specific Order Unique Identifier 
        :param header is required for set Content-Type and authorization"""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def modify_order(self, appOrderID, modifiedProductType, modifiedOrderType, modifiedOrderQuantity,
                     modifiedDisclosedQuantity, modifiedLimitPrice, modifiedStopPrice, modifiedTimeInForce,
                     orderUniqueIdentifier, clientID):
        try:
            appOrderID = int(appOrderID)
            clientID = clientID
            end_point = configParser.get('interactive_endpoints', 'modifyorder')
            modify_data = {'appOrderID': appOrderID, 'modifiedProductType': modifiedProductType,
                           'modifiedOrderType': modifiedOrderType, 'modifiedOrderQuantity': modifiedOrderQuantity,
                           'modifiedDisclosedQuantity': modifiedDisclosedQuantity,
                           'modifiedLimitPrice': modifiedLimitPrice,
                           'modifiedStopPrice': modifiedStopPrice, 'modifiedTimeInForce': modifiedTimeInForce,
                           'orderUniqueIdentifier': orderUniqueIdentifier
                           }
            if not isInvestorClient:
                modify_data['clientID'] = clientID
            else:
                pass
            s = requests.Session()
            url = port + prefix + end_point
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.put(url, data=json.dumps(modify_data), headers=headers, verify=False)
            print(f'\nModified Order:{response.json()}')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class OrderBook:
    """Order book required for states of all the orders placed by an user like pending,new,replace etc. """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_orderbook(self):
        try:
            endpoint = configParser.get('interactive_endpoints', 'getorderbook')
            url = port + prefix + endpoint
            get_orderbook_data = {}
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.get(url, data=json.dumps(get_orderbook_data), headers=headers, verify=False)
            print(f'\nOrder Book:{response.json()}')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Tradebook():
    """trade required  list of all trades executed on a particular day """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_trade(self, clientID):
        try:
            endpoint = configParser.get('interactive_endpoints', 'gettradebook')
            url = port + prefix + endpoint

            payload = {'clientID': clientID}
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.get(url, params=payload, headers=headers, verify=False)
            print(f'\nTrade Book:{response.json()}')

            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Holding:
    """holdings"""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    def get_holding(self, clientID):
        try:
            end_point = configParser.get('interactive_endpoints', 'getholding')
            payload = {}
            if not isInvestorClient:
                payload['ClientID'] = clientID
            else:
                pass

            url = port + prefix + end_point
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.get(url, params=payload, headers=headers, verify=False)
            print(f'\nHoldings :{response.json()}')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Position:
    """ positions API returns two sets of positions, net and day. """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_Positionday(self, clientID):
        try:
            end_point = configParser.get('interactive_endpoints', 'getposition')
            payload = {'dayOrNet': 'DayWise'}
            if not isInvestorClient:
                payload['ClientID'] = clientID
            else:
                pass

            url = port + prefix + end_point
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.get(url, params=payload, headers=headers, verify=False)
            print(f'\nPostion by day :{response.json()}')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)

    def get_Positionnet(self, clientID):
        try:
            end_point = configParser.get('interactive_endpoints', 'getposition')
            payload = {'dayOrNet': 'NetWise'}
            if not isInvestorClient:
                payload['ClientID'] = clientID
            else:
                pass
            url = port + prefix + end_point
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.get(url, params=payload, headers=headers, verify=False)
            print(f'\nPosition by net: {response.json()}')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Position_convert:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    def position_Convert(self, exchangeSegment, exchangeInstrumentID, targetQty, isDayWise, oldProductType,
                         newProductType, clientID):
        try:
            position_place_data = {'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID,
                                   'targetQty': targetQty, 'isDayWise': isDayWise, 'oldProductType': oldProductType,
                                   'newProductType': newProductType}
            end_point = configParser.get('interactive_endpoints', 'positionconvert')
            payload = {}
            if not isInvestorClient:
                payload['ClientID'] = clientID
            else:
                pass
            url = port + prefix + end_point
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.put(url, data=json.dumps(position_place_data), params=payload, headers=headers, verify=False)
            print('\nPosition Convert:')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class CancelOrder:
    """appOrderID : required for cancel the order"""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def cancel_order(self, appOrderID, orderUniqueIdentifier, clientID):
        try:
            end_point = configParser.get('interactive_endpoints', 'cancelorder')
            payload = {'appOrderID': appOrderID, 'orderUniqueIdentifier': orderUniqueIdentifier}
            if not isInvestorClient:
                payload['ClientID': clientID]
            else:
                pass
            url = port + prefix + end_point
            s = requests.Session()
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.delete(url, params=payload, headers=headers, verify=False)
            print(f'\nCancel Order: {response.json()}')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Place_cover():
    """
        :param exchangeSegment required for which represents cash, derivative, commodity or currency market.
        :param exchangeInstrumentID required for Instrument Unique ID.
        :param productType required for identify the category of the order like CNC,NRML,MIS etc.
        :param timeInForce is required to indicate how long order will remain active.
        :param disclosedQuantity is an order in which only a part of the order quantity is disclosed to the market
        :param orderQuantity is the number of Sell or Buy orders
        :param limitPrice is a price used during a limit order when buying a security
        :param stopPrice is the price in a stop order that triggers the creation of a market order.
        :param orderUniqueIdentifier is user specific Order Unique Identifier 
        :param header is required for set Content-Type and authorization
        """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def place_coverorder(self, exchangeSegment, exchangeInstrumentID, orderSide, orderQuantity, disclosedQuantity,
                         limitPrice, stopPrice, orderUniqueIdentifier, clientID):
        try:
            s = requests.Session()
            end_point = configParser.get('interactive_endpoints', 'placecover')
            cv_data = {'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID,
                       'orderSide': orderSide, 'orderQuantity': orderQuantity, 'disclosedQuantity': disclosedQuantity,
                       'limitPrice': limitPrice, 'stopPrice': stopPrice, 'orderUniqueIdentifier': orderUniqueIdentifier}
            payload = {}
            if not isInvestorClient:
                payload['ClientID': clientID]
            else:
                pass
            url = port + prefix + end_point
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.post(url, data=json.dumps(cv_data), params=payload, headers=headers, verify=False)
            print(f"Place cover: {response.json()}")
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Exitcover:
    """
        :param appOrderID is required to generate unique order number
        :param header is required for set Content-Type and authorization

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def exitcover_order(self, appOrderID, clientID):
        try:
            appOrderID = int(appOrderID)
            s = requests.Session()
            exdata = {'appOrderID': appOrderID}
            payload = {}
            if not isInvestorClient:
                payload['ClientID': clientID]
            else:
                pass
            url = port + prefix + end_point
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.put(url, data=json.dumps(exdata), params=payload, headers=headers, verify=False)
            print(f'\nExitcover: {response.json}')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Squareoff():
    """
        :param exchangeSegment required for which represents cash, derivative, commodity or currency market.
        :param exchangeInstrumentID required for Instrument Unique ID.
        :param productType required for identify the category of the order like CNC,NRML,MIS etc.
        :param squareoffMode is a mode like daywise or netwise
        :param squareoffQtyValue is a type os square quantiy like ExactQty or Percentage 
        :param header is required for set Content-Type and authorization
        """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def squareoff(self, exchangeSegment, exchangeInstrumentID, productType, squareoffMode,
                  positionSquareOffQuantityType, squareOffQtyValue, blockOrderSending, cancelOrders, clientID):
        try:
            s = requests.Session()
            sqdata = {'exchangeSegment': exchangeSegment, 'exchangeInstrumentID': exchangeInstrumentID,
                      'productType': productType, 'squareoffMode': squareoffMode, 'positionSquareOffQuantityType': positionSquareOffQuantityType,
                      'squareOffQtyValue': squareOffQtyValue, 'blockOrderSending': blockOrderSending, 'cancelOrders': cancelOrders
                      }
            payload = {}
            end_point = configParser.get('interactive_endpoints', 'squareoff')
            if not isInvestorClient:
                payload['ClientID'] = clientID
            else:
                pass
            url = port + prefix + end_point
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})
            response = s.put(url, data=json.dumps(sqdata), params=payload, headers=headers, verify=False)
            print(f'\nSquareoff: {response.json()}')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class OrderHistory:
    """appOrderID : required for cancelling the order"""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_orderhistory(self, appOrderID, clientID):
        try:
            end_point = configParser.get('interactive_endpoints', 'orderhistory')
            payload = {'appOrderID': appOrderID}
            if not isInvestorClient:
                payload['ClientID': clientID]
            else:
                pass
            url = port + prefix + end_point
            headers.update({'Content-Type': 'application/json', 'Authorization': tokenn})

            s = requests.Session()
            response = s.get(url, params=payload, headers=headers, verify=False)

            print(f'\nOrder History: {response.json()}')
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)


class Logout():
    """Required for destroys api session and token"""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def logout(self):
        try:
            end_point = configParser.get('interactive_endpoints', 'logout')
            url = port + prefix + end_point
            headers.update({'authorization': tokenn})
            s = requests.Session()

            response = s.delete(url, headers=headers, verify=False)

            print("--------------------------------------------------------")
            print(response)
            print("--------------------------------------------------------")
            print(f'Log-out Successful:{response.json()}')
            print("--------------------------------------------------------")
            raise ExceptionHandle
        except ExceptionHandle:
            ExceptionHandle.checkResponse(response)
