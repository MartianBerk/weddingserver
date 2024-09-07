from copy import deepcopy
from typing import Dict

from baked.lib.dbaccess.public import DbAccess, ColumnFactory, ColumnModelFactory
from baked.lib.globals import get_global
from baked.lib.wedding.model.guest import Guest


class WeddingService:

    _db = "wedding"
    _table = "guests"
    _valid_rsvp = ("CEREMONY", "PARTY", "NONE",)

    def __init__(self):
        db_settings: Dict = get_global("dbs", self._db)

        self._driver = db_settings.get("driver")
        self._db = DbAccess.connect(self._driver,
                                    self._db,
                                    db_settings.get("location"))
        
    @property
    def valid_rsvp(self):
        return deepcopy(self._valid_rsvp)
        
    def get_guest(self, guest_id: int):
        pass
        
    def rsvp(self, guest: Guest, rsvp: str):
        if rsvp.upper() not in self._valid_rsvp:
            raise ValueError("Invalid RSVP value")

        guest.rsvp = rsvp
        guest: Dict = guest.to_dict()

        column_class = ColumnFactory.get(self._driver)
        self._db.update(
            self._table,
            ColumnModelFactory.get(self._driver)(
                [
                    column_class(key, Guest.get_sql_datatype(key), value=value)
                    for key, value in guest.items()
                ]
            )
        )