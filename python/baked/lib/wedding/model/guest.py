from baked.lib.model import Model


class Guest(Model):
    _attributes = {
        "email": str,
        "firstname": str,
        "invite": str,
        "lastname": str,
        "user_id": int,
        "rsvp": str,
        "diet": str
    }

    @classmethod
    def attribute_map(cls):
        return cls._attributes

    @classmethod
    def optional_attributes(cls):
        return ["rsvp", "diet"]

    @classmethod
    def auto_attributes(cls):
        return []

    @classmethod
    def public_attributes(cls):
        return ["firstname", "lastname", "rsvp", "diet"]

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
                "rsvp": self.rsvp,
                "email": self.email,
                "diet": self.diet
            }

        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "invite": self.invite,
            "rsvp": self.rsvp,
            "user_id": self.user_id,
            "email": self.email,
            "diet": self.diet
        }
    
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
        return self._rsvp
    
    @rsvp.setter
    def rsvp(self, value):
        self._rsvp = value

    @property
    def diet(self):
        return self._diet
    
    @diet.setter
    def diet(self, value):
        self._diet = value
