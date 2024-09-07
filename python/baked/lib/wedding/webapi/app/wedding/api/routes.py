from typing import *

from baked.lib.accesscontrol.error import InvalidPassword, KeyNotSet, InvalidKey
from baked.lib.accesscontrol.webapi.useraccess import UserAccess
from baked.lib.webapi import request, response
from baked.lib.wedding.service.weddingservice import WeddingService

from .. import wedding


@wedding.route("/", methods=["GET"], open_url=True)
def index():
    return response({"message": "Up and running..."}), 200


@wedding.route("/auth", methods=["POST"], open_url=True)
def auth():
    body: Dict = request.json
    if "token" not in body or "email" not in body:
        return response({"error": True, "message": "Invalid payload"}), 500
    
    try:
        # Having given each guest a QR code containing a token, we auto-authenticate for them.
        acl = UserAccess.load_from_identity("email", body["email"])
        acl.check_user()

        if not acl.authenticate():
            try:
                acl.login(body["token"])
                rtn_response = response({"is_logged_in": True, **acl.user.to_dict(public_only=True)})

                cookie_expiry_secs = acl.cookie_expiry_hours * 3600 if acl.cookie_expiry_hours else None
                rtn_response.set_cookie("bkuid", str(acl.user.id).encode(), max_age=cookie_expiry_secs)
                rtn_response.set_cookie("bkaccess", str(acl.access_key).encode(), max_age=cookie_expiry_secs)
                rtn_response.set_cookie("bkrefresh", str(acl.refresh_key).encode(), max_age=cookie_expiry_secs)

                return rtn_response

            except InvalidPassword:
                return response({"error": True, "message": "Invalid Credentials"}), 403

    except (KeyNotSet, InvalidKey):
        return response({"error": True, "message": "Invalid Credentials"}), 403

    except Exception:
        return response({"error": True, "message": f"Something Went Wrong"}), 500


@wedding.route("/rsvp", methods=["POST"])
def rsvp():
    body: Dict = request.json
    if "rsvp" not in body:
        return response({"error": True, "message": "Invalid payload"}), 500
    
    guest_rsvps = []
    service = WeddingService()
    
    for r in body["rsvp"]:
        if "guest_id" not in r or "rsvp" not in r:
            return response({"error": True, "message": "Invalid payload"}), 500
        
        if r["rsvp"].upper() not in service.valid_rsvp:
            return response({"error": True, "message": "Invalid payload"}), 500
        
        guest = service.get_guest(r["guest_id"])
        if not guest:
            return response({"error": True, "message": "Unknown guest"}), 500
        
        guest_rsvps.append((guest, r["rsvp"],))

    for guest_rsvp in guest_rsvps:
        service.rsvp(guest_rsvp[0], guest_rsvp[1])

    return response({"guests": [g[0].to_dict(public_only=True)] for g in guest_rsvps}), 200
