from baked.lib.model import Model


class AccountData(Model):

    @classmethod
    def attributes(cls):
        return []

    @classmethod
    def attribute_map(cls):
        return {}

    @classmethod
    def optional_attributes(cls):
        return []

    @classmethod
    def auto_attributes(cls):
        return []

    @classmethod
    def public_attributes(cls):
        return []

    @classmethod
    def deserialize(cls, **kwargs):
        return cls(**kwargs)

    def to_dict(self, public_only=False):
        return {}

    def update(self, **kwargs):
        return None
