from typing import *

from baked.lib.accesscontrol.error import InvalidPassword, KeyNotSet, InvalidKey
from baked.lib.accesscontrol.webapi.useraccess import UserAccess
from baked.lib.webapi import request, response
from baked.lib.wedding.model.guest import Guest
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
    

@wedding.route("/guest", methods=["GET", "POST"], permissions=["ADMIN"])
def guest():
    service = WeddingService()

    if request.method == "POST":
        body = request.json
        for key in ("firstname", "lastname", "email", "user_id", "invite",):
            if key not in body:
                return response({"error": True, "message": "Invalid payload"}), 500
        
        guest = Guest(**body)
        service.create_guest(guest)

        return response({"guest": guest.to_dict()}), 200

    if request.method == "GET":
        email = request.args.get("email")
        if not email:
            guests = service.list_guests()
            return response({"guests": [g.to_dict() for g in guests]}), 200

        guest: Guest = service.get_guest(email)
        return response({"guest": guest.to_dict() if guest else {}}), 200


@wedding.route("/rsvp", methods=["POST"])
def rsvp():
    body: Dict = request.json
    if "rsvp" not in body:
        return response({"error": True, "message": "Invalid payload"}), 500
    
    # Locked URI, must have supplied to have gotten this far, unless tampering.
    uid = request.cookies.get("bkuid")
    
    guest_rsvps = []
    service = WeddingService()
    
    for r in body["rsvp"]:
        if "email" not in r or "rsvp" not in r:
            return response({"error": True, "message": "Invalid payload"}), 500
        
        if r["rsvp"].upper() not in service.valid_rsvp:
            return response({"error": True, "message": "Invalid payload"}), 500
        
        # TODO: Test to make sure this UID lock works.
        guest = service.get_guest(r["email"], user_id=uid)
        if not guest:
            return response({"error": True, "message": "Unknown guest"}), 500
        
        guest_rsvps.append((guest, r["rsvp"],))

    for guest_rsvp in guest_rsvps:
        service.rsvp(guest_rsvp[0], guest_rsvp[1])

    return response({"guests": [g[0].to_dict(public_only=True)] for g in guest_rsvps}), 200
