import configparser
from datetime import datetime

from Connect import XTSConnect
from MarketDataSocketClient import MDSocket_io

# logging.basicConfig(level=logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------------------
# Market Data
# ----------------------------------------------------------------------------------------------------------------------

cfg = configparser.ConfigParser()
cfg.read('config.ini')

# MarketData API Credentials
API_KEY     = cfg.get('market', 'apiKey')
API_SECRET  = cfg.get('market', 'apiSecret')
SOURCE      = cfg.get('user', 'source')

# Initialise
xt = XTSConnect(API_KEY, API_SECRET, SOURCE)

# Login for authorization token
response = xt.marketdata_login()

# Store the token and userid
set_marketDataToken = response['result']['token']
set_muserID = response['result']['userID']
# print("Login: ", response)

# Connecting to Marketdata socket
soc = MDSocket_io(set_marketDataToken, set_muserID)

# Instruments for subscribing
Instruments = [{'exchangeSegment': 1, 'exchangeInstrumentID': "NIFTY 50"}]

# Callback for connection
def on_connect():
    """Connect from the socket."""
    print('Market Data Socket connected successfully!')

    # Subscribe to instruments
    print('Sending subscription request')
    response = xt.send_subscription(Instruments, 1504)
    print('Sent Subscription request!')
    print("Subscription response: ", response)


# Callback on receiving message
def on_message(data):
    print('I received a message!')

# Callback for message code 1501 FULL
def on_message1501_json_full(data):
    print('I received a 1501 Level1,Touchline message!' + data)

# Callback for message code 1501 PARTIAL
def on_message1501_json_partial(data):
    print('I received a 1501, Instrument Property Change Event message!' + data)

# Callback for message code 1504 FULL
def on_message1504_json_full(data):
    print('I received a 1504 Index data message!' + data)

# Callback for message code 1504 PARTIAL
def on_message1504_json_partial(data):
    print('I received a 1504 Index data message!' + data)

# Callback for disconnection
def on_disconnect():
    print('Market Data Socket disconnected!')


# Callback for error
def on_error(data):
    """Error from the socket."""
    print('Market Data Error', data)

# Assign the callbacks.
soc.on_connect = on_connect
soc.on_message = on_message
soc.on_message1501_json_full = on_message1501_json_full
soc.on_message1501_json_partial = on_message1501_json_partial
# soc.on_message1504_json_full = on_message1504_json_full
# soc.on_message1504_json_partial = on_message1504_json_partial
soc.on_disconnect = on_disconnect
soc.on_error = on_error

# Event listener
el = soc.get_emitter()
el.on('connect', on_connect)
el.on('1501-json-full', on_message1501_json_full)

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
soc.connect()