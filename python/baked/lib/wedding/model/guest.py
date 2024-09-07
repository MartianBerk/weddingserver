from baked.lib.model import Model


class Guest(Model):
    _attributes = {
        "id": int,
        "email": str,
        "firstname": str,
        "invite": str,
        "lastname": str,
        "user_id": int,
        "rsvp": bool
    }

    @classmethod
    def attribute_map(cls):
        return cls._attributes

    @classmethod
    def optional_attributes(cls):
        return []

    @classmethod
    def auto_attributes(cls):
        return []

    @classmethod
    def public_attributes(cls):
        return ["firstname", "lastname", "rsvp"]

    @classmethod
    def get_sql_datatype(cls, item):
        try:
            return {
                int: "int",
                str: "str",
                bool: "bool"
            }[cls._attributes[item]]

        except KeyError:
            raise ValueError("unknown item")

    def to_dict(self, public_only=False):
        if public_only:
            return {
                "firstname": self.firstname,
                "lastname": self.lastname,
                "invite": self.invite,
                "rsvp": self.rsvp
            }

        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "invite": self.invite,
            "rsvp": self.rsvp,
            "user_id": self.user_id
        }

    @property
    def id(self):
        return self._id
    
    @property
    def email(self):
        return self._email

    @property
    def firstname(self):
        return self._firstname
    
    @property
    def invite(self):
        return self._invite

    @property
    def lastname(self):
        return self._lastname
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def rsvp(self):
        return self._rsvp or False
    
    @rsvp.setter
    def rsvp(self, value):
        self._rsvp = value
