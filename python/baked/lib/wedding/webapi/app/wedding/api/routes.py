from typing import *

from baked.lib.accesscontrol.error import InvalidPassword, KeyNotSet, InvalidKey
from baked.lib.accesscontrol.webapi.useraccess import UserAccess
from baked.lib.webapi import request, response

from .. import wedding


@wedding.route("/", subdomains=["api"], methods=["GET"], open_url=True)
def index():
    return response({"message": "Up and running..."})


@wedding.route("/auth", subdomains=["api"], methods=["POST"], open_url=True)
def auth():
    body: Dict = request.json
    if "token" not in body or "email" not in body:
        return response({"error": True, "message": "Invalid Credentials"})
    
    try:
        # Having given each guest a QR code containing a token, we auto-authenticate for them.
        acl = UserAccess.load_from_identity("email", body["email"])
        acl.check_user()

        if not acl.authenticate():
            try:
                acl.login(body["token"])

            except InvalidPassword:
                return response({"error": True, "message": "Invalid Credentials"})

    except (KeyNotSet, InvalidKey):
        return response({"error": True, "message": "Invalid Credentials"})

    except Exception as e:
        return response({"error": True, "message": f"Something Went Wrong: {str(e)}"})


@wedding.route("/rsvp", subdomains=["api"], methods=["POST"])
def rsvp():
    pass

