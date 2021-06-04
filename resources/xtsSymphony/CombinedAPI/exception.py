import requests
import json
from requests import exceptions
from requests.exceptions import HTTPError
from requests import ConnectTimeout, HTTPError, Timeout, ConnectionError

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                Here we have declared all the exception and responses
    If there is any exception occurred we have this code to convey the messages
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class InputError(Exception):
    pass


class ExceptionHandle(Exception):
    """initializing the exception.."""

    def __init__(self):
        pass

    def checkResponse(self, Request_login=None, InputError=None):
        try:
            if self.status_code == 200:
                print('Successful')
            elif self.status_code == 404:
                print('Page Not Found')
                print(self.text)
            elif self.status_code == 400:
                print('bad Request Found')
                print(self.text)
            elif self.status_code != 200:
                raise InputError
            else:
                self.raise_for_status()
        except requests.exceptions.ConnectionError as errc:
            print("Connection Error", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except InputError:
            print('Try again... ')
            Request_login.login()
        except KeyError as key_err:
            print(f'Invalid credentials, please try again... {key_err}')
        except NameError:
            print('Response Name is not defined')
        except Exception as err:
            print(f'Unknown error occurred: {err}')
