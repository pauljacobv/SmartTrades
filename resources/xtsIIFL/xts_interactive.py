import configparser
from Connect import XTSConnect

# logging.basicConfig(level=logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------------------
# Interactive
# ----------------------------------------------------------------------------------------------------------------------

cfg = configparser.ConfigParser()
cfg.read('config.ini')

# Interactive API Credentials
API_KEY     = cfg.get('interactive', 'apiKey')
API_SECRET  = cfg.get('interactive', 'apiSecret')
SOURCE      = cfg.get('user', 'source')

"""Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
xt = XTSConnect(API_KEY, API_SECRET, SOURCE)

"""Using the xt object we created call the interactive login Request"""
response = xt.interactive_login()
print("Login: ", response)

"""Order book Request"""
response = xt.get_order_book()
print("Order Book: ", response)