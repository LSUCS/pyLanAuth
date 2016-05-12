"""
Wrapper class for the LAN website API
"""
import logging
import requests
from requests.exceptions import ConnectionError

# Setup logger
logging.getLogger("urllib3").setLevel(logging.WARNING)


class LanWebsiteAPI(object):
    """
    Interface to the lan website API.
    """
    
    def __init__(self, base_url, apikey):
        self.base_url = base_url
        self.apikey = apikey

    def lan_number(self):
        """
        Fetches the current lan number
        :returns int:   Lan Number
        """
        url = self.base_url + '/api/lannumber'
        try:
            req = requests.get(url)
            req.raise_for_status()
        except ConnectionError:
            raise APIError("Error connecting to the LAN API")

        return int(req.json()['lan'])


    def lan_auth(self, username, password, seat):
        """
        Check credentials and seat with the LAN website.
        """
        data = {
            "api_key": self.apikey,
            "username": username,
            "password": password,
            "seat": seat
        }

        url = self.base_url + '/api/Lanauth'
        try:
            req = requests.post(url, data=data)
            req.raise_for_status()
        except ConnectionError:
            raise APIError("Error connecting to the LAN API")

        response = req.json()
        if response == 1:
            return True
        elif "error" in response:
            raise APIError(response['error'])
        else:
            raise APIError("Something went right")


class APIError(Exception):
    """Exception for api errors"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "APIError: %s" % repr(self.value)


# Self test
if __name__ == '__main__':
    
    # Key for talking to the HTTP api
    APIKEY = 'L$uc$7anap1k3y'
    BASE_URL = 'https://dev.lan.lsucs.org.uk'

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', required=True, help='Username')
    parser.add_argument('-p', required=True, help='Password')
    parser.add_argument('-s', required=True, help='Seat')
    args = parser.parse_args()

    api = LANWebsiteAPI(BASE_URL, APIKEY)
    
    try:
        api.lanauth(args.u, args.p, args.s)
    except APIError as error:
        print("Exception when testing lanauth: %s" % str(error))
