"""
Background daemon for opening the firewall
"""
import logging
import time

from lanauth.db import load_db, open_session
from lanauth.db.models import Authentications
from lanauth.config import SiteConfig 
from lanauth.device import Device
from lanauth.lan_api import LanWebsiteAPI

logger = logging.getLogger(__name__)


class Daemon():
    """
    Worker for opening access to the firewall
    """
    
    def __init__(self, config):
        self.interval = config.get('daemon', 'interval', fallback=30)
    
        name     = config.get('device', 'name')
        address  = config.get('device', 'address')
        port     = config.getint('device', 'port')
        username = config.get('device', 'username')
        keyfile  = config.get('device', 'keyfile')
        cmd      = config.get('device', 'cmd')

        lw_url = config.get('lan_api', 'url')
        lw_apikey = config.get('lan_api', 'key')
        lw_api = LanWebsiteAPI(lw_url, lw_apikey)

        lan_number = lw_api.lan_number()

        self.device = Device(name, address, port, username, keyfile, cmd, lan_number)


    def _work(self):
        """Work function for daemon
        
        Fetches the current auth queue and attempts to authenticate
        each entry.
        """
        sucessful = []
        with open_session() as session:
            queue = session.query(Authentications) \
                       .filter(Authentications.status==False).all()

            for auth in queue:
                try:
                    logger.info("Attempting to authenticate: %s %s" % (auth.username, auth.ip_addr))
                    self.device.allow_ip(auth.username, auth.ip_addr)
                    sucessful.append(auth)
                except Exception as error:
                    raise error

                # Flag entry as sucessful
                for entry in sucessful:
                    entry.status = True
                    session.flush()


    def start(self):
        """Entry point for the daemon

        Run forever until stopped
        """
        while True:
            try:
                self._work()
            except KeyboardInterrupt:
                logger.info("Stopping deamon")
                break
            except Exception as error:
                logger.execption("Exception in daemon: %s" % str(error))
                break

            # Sleep for interval and gracefully handle keyboard interrupts
            logger.info("Sleeping for %s seconds" % self.interval)
            try:
                time.sleep(self.interval)
            except KeyboardInterrupt:
                logger.info("Stopping deamon")
                return

