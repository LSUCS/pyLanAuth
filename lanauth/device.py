"""
"""
KEYFILE = "./router.key"

import shlex
from subprocess import call


class Device(object):
    """
    Router device interface

    Wrapper for talking to the relevent firewall device
    """

    def __init__(self, name, address, port, remote_user, keyfile, cmd, lan_number):
        self.name = name
        self.address = address
        self.port = port
        self.remote_user = remote_user
        self.keyfile = keyfile
        self.cmd = cmd
        self.lan_number = lan_number


    def allow_ip(self, username, user_ip):
        """
        Authenticate a user on the firewall
        
        :param username: Username for rule reference
        :param ip_addr:  IP to allow in the firewall
        """

        cmd = "ssh -o StrictHostKeyChecking=no -i %s %s@%s %s %i %s %s" % (
            # Router
            self.keyfile,
            self.remote_user,
            self.address,
            self.cmd,

            # User
            self.lan_number,
            username.replace(" ", "").replace("'", ""),
            user_ip
        )    

        args = shlex.split(cmd)
        call(args)

