"""
Messy utilities to do everything
"""

KEYFILE = "./router.key"

import shlex
from subprocess import call


def do_ssh(lan_number, username, ip_addr):
    cmd = "ssh -i %s lsucs@192.168.0.1 /home/lsucs/lan-auth.sh %i %s %s" % (
        KEYFILE, lan_number, username, ip_addr
    )    
    args = shlex.split(cmd)

    call(args)


if __name__ == '__main__':
    do_ssh(57, "sirboldilox", "192.168.0.51")
