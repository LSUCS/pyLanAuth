#!/bin/sh

# Add a user's IP address to the EdgeOS Firewall
# e.g. ./lan-auth.sh 48 oliverw92 192.168.0.82
echo "$@$@"


################
# START CONFIG #

AUTH_GROUP=authed_lan_users

#  END CONFIG  #
################

# Execute commands without running configure
run=/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper

# Go into config mode
$run begin

# Add users IP to firewall group
$run set firewall group address-group $AUTH_GROUP address $3
echo "Added $3 to $AUTH_GROUP"

# Commit
$run commit
$run end
