import os
from urllib.parse import urljoin

import requests
from requests.exceptions import HTTPError, ConnectionError

DEFAULT_MINUTES = 5760  #: 4 days


class Unifi(object):

    def __init__(self, base_url, username, password, minutes=DEFAULT_MINUTES):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.default_minutes = minutes

        self._cookies = {}


    def login(self):
        """ Authorize this session with the unifi controller.
        """
        params = {
            "username": self.username,
            "password": self.password
        }

        try:
            resp = requests.post(urljoin(self.base_url, "/api/login"), json=params, verify=False)
            resp.raise_for_status()
        except (HTTPError, ConnectionError) as error:
            raise UnifiError(str(error))

        self._cookies = resp.cookies
        return True

    def authorize(self, site, mac_addr, minutes=None):
        """ Allow a guest access on the specific site.

        :param site:        Site
        :param mac_addr:    Guest ID
        :param minutes:     Number of minutes to allow access for.
        """
        if minutes is None:
            minutes = self.default_minutes

        params = {
            "cmd": "authorize-guest",
            "mac": mac_addr,
            "minutes": minutes
        }

        try:
            resp = requests.post(urljoin(self.base_url, os.path.join("api/s/%s/cmd/stamgr" % site)),
                                 json=params, cookies=self._cookies, verify=False)
            resp.raise_for_status()
        except (HTTPError, ConnectionError) as error:
            raise UnifiError(str(error))

        return True


class UnifiError(Exception):
    pass
