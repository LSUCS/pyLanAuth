"""
Entry point script for the app
"""
import logging
from configparser import Error as ConfigError

from lanauth.app import app_factory
from lanauth.admin import app as admin_blueprint
from lanauth.config import SiteConfig
from lanauth.db import load_db



def load_config(config_file):
    # Load the config
    try:
        return SiteConfig.from_file(config_file)
    except ConfigError as error:
        print("Exception in config: %s" % error)
        return None

def load_app(config):
    """Build the flask application
    
    Most of this can be moved into the app_factory function
    """
    load_db(config)

    blueprints = [
        (admin_blueprint, "/admin")
    ]
    app = app_factory("lanauth", config, blueprints)

    # Load the webserver
    app.iniconfig = config
    app.secret_key = config.get('flask', 'secret_key')
    app.debug = config.getboolean('flask', 'debug', fallback=False)
    return app


def cli():
    """Entry point for command line script"""
    import argparse

    parser = argparse.ArgumentParser(
        description="LAN Auth Webserver"
    )
    parser.add_argument('-c', '--config', required=True, help="Config file to load")
    subparsers = parser.add_subparsers(help='Commands', dest='cmd')

    parser_add = subparsers.add_parser('add', help='Add an entry to the Auth table')
    parser_add.add_argument('username', help="Name")
    parser_add.add_argument('ip', help="IP address")
    parser_add.add_argument('seat', help="IP address")

    parser_add = subparsers.add_parser('daemon', help='Run the authentication daemon')

    args = parser.parse_args()

    config = load_config(args.config)
    if config is None:
        print("Failed to parse file: " % config)

    # Add a new auth entry
    if args.cmd == 'add':
        from lanauth.db import open_session
        from lanauth.db.models import Authentications
        from lanauth.lan_api import LanWebsiteAPI
        load_db()
        lanapi = LanWebsiteAPI(
            config['lan_api']['url'],
            config['lan_api']['key']
        )

        ip_addr = args.ip
        username = args.username 
        seat = args.seat
        lan = lanapi.lan_number()

        with open_session() as session:
            auth = Authentications.add(session, ip_addr, lan, username, seat)
            print("Added: %s" % auth)


    # Run the authentication daemon
    elif args.cmd == 'daemon':
        from lanauth.daemon import Daemon
        rootLogger = logging.getLogger('')
        rootLogger.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        filelogger = logging.FileHandler('/srv/http/lanauth/log')
        filelogger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)-15s %(levelname)-8s %(name)-15s %(message)s')
        console.setFormatter(formatter)
        filelogger.setFormatter(formatter)

        rootLogger.addHandler(filelogger)
        rootLogger.addHandler(console)
        rootLogger.info('LANAUTH Daemon') 

        load_db(config)
        daemon = Daemon(config)
        daemon.start()

    # Run the webserver
    else:
        app = load_app(config)

        host  = config.get('flask', 'host', fallback='127.0.0.1')
        port  = config.getint('flask', 'port', fallback=8080)
        app.run(host=host, port=port, use_reloader=False)

def uwsgi():
    """Entry point for uwsgi"""
    config = load_config(args.config)
    if config is not None:
        app = load_app(config)
        return app

# Make script runnable
if __name__ == '__main__':
    cli()
