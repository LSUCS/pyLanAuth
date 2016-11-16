"""
Internal API

* **/api/check**  Check if user is already authed
* **/api/auth**   Check username, password and seat
"""

from flask import jsonify, request, current_app
from flask_restful import Api, Resource, reqparse

# Local imports
from lanauth.db import open_session
from lanauth.db.models import Authentications, AuthQueue
from lanauth.lan_api import LanWebsiteAPI, APIError



class CheckAPI(Resource):
    """API handler checking a users auth status

    **GET** http://<base url>/api/check

    Example response::

        {
            "status": 0
        }

    """
    STATUS_NO_AUTH = 0      #: User has not yet authenticated
    STATUS_PENDING = 1      #: Authentication is pending
    STATUS_AUTH    = 2      #: User is authenticated

    def get(self):
        response = {}
        lw_url = current_app.iniconfig.get('lan_api', 'url')
        lw_apikey = current_app.iniconfig.get('lan_api', 'key')

        # Fetch lan number
        lw_api = LanWebsiteAPI(lw_url, lw_apikey)
        try:
            lan_number = lw_api.lan_number()
        except APIError as error:
            return jsonify({"status": STATUS_NO_AUTH})
            
        # Incase the server is running behind a proxy
        ip_addr = request.remote_addr

        response = {}
        pending = False
        complete = False

        # Check if user is already authenticated
        auth = None
        with open_session() as session:
            auth = session.query(Authentications) \
                .filter(Authentications.lan == lan_number) \
                .filter(Authentications.ip_addr == ip_addr).first()

            # Check if pending
            if auth is not None:
                if auth.status:
                    complete = True
                else:
                    pending = True

        # Auth complete
        if complete:
            response['status'] = self.STATUS_AUTH

        # Authentication pending
        elif pending:
            response['status'] = self.STATUS_PENDING

        # User not authenitcated
        else:
            response['status'] = self.STATUS_NO_AUTH

        # Return  response JSON
        return jsonify(response)

    @staticmethod
    def add(api):
        api.add_resource(CheckAPI, '/api/check')


class AuthAPI(Resource):
    """
    API handler for checking username and passwords

    **POST** http://<base url>/api/auth

    JSON Body::

        {
            "username": "Bob",
            "password": "bobBob1234"
            "seat":     "a1"
        }

    Example response::

        {
            "status": 0
            "error": "Additional error message"
        }

    """
    STATUS_PASS = 0     #: Auth was sucessful
    STATUS_FAIL = 1     #: Auth failed

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', required=True)
    parser.add_argument('seat', required=True)

    def post(self):

        # Parse arguments
        args = self.parser.parse_args(strict=True)

        lw_url = current_app.iniconfig.get('lan_api', 'url')
        lw_apikey = current_app.iniconfig.get('lan_api', 'key')

        # Valide user credentials
        lw_api = LanWebsiteAPI(lw_url, lw_apikey)

        response = {}
        try:
            lw_api.lan_auth(args.username, args.password, args.seat)
            lan_number = lw_api.lan_number()
            response['status'] = self.STATUS_PASS
        except APIError as error:
            response['status'] = self.STATUS_FAIL
            response['error'] = error.value

            current_app.logger.error(error)
            return jsonify(response)

        # Add database entry
        ip_addr = request.remote_addr
        with open_session() as session:
            auth_check = session.query(Authentications) \
                           .filter(Authentications.lan == lan_number) \
                           .filter(Authentications.ip_addr == ip_addr) \
                           .first()

            # If true user IP has alread authenticated
            if auth_check:
                return jsonify(response)

            # Add new record
            auth = Authentications.add(session, ip_addr, lan_number, args.username, args.seat)

        current_app.logger.info("Authentication added for: %s IP: %s" %
                (args.username, ip_addr)
            )

        return jsonify(response)

    @staticmethod
    def add(api):
        api.add_resource(AuthAPI, '/api/auth')


# Load the api
def load_api(app):
    api = Api(app)
    for resource in Resource.__subclasses__():
        resource.add(api)
