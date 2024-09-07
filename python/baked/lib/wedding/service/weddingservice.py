from copy import deepcopy
from typing import Dict, Optional, Union

from baked.lib.dbaccess.public import DbAccess, ColumnFactory, ColumnModelFactory, FilterFactory, AndFilterModel
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
    
    def _get_column_model(self, guest: Optional[Dict] = None, filters: Optional[Dict] = None):
        column_class = ColumnFactory.get(self._driver)

        if not guest:
            columns = {c: None for c in self._db.get_columns(self._table)}
        elif filters:
            columns = [column_class(k, Guest.get_sql_datatype(k), value=v) for k, v in filters.items()]
        else:
            columns = [
                column_class(key, Guest.get_sql_datatype(key), value=value)
                for key, value in guest.items()
            ]

        ColumnModelFactory.get(self._driver)(columns) 
    
    def list_guests(self):
        guests = self._db.get(self._table, self._get_column_model())
        return [Guest(**g) for g in guests]

    def get_guest(self, guest_id: Optional[int] = None, email: Optional[str] = None) -> Union[Guest, None]:
        if guest_id:
            filters = {"id": guest_id}
        elif email:
            filters = {"email": email}

        column_model = self._get_column_model(filters=filters)

        filter_class = FilterFactory.get(self._driver)
        filters = [filter_class(c, "equalto") for c in column_model.columns]
        filter_model = AndFilterModel(filters)

        guest = self._db.get(self._table, column_model, filter_model=filter_model)
        if not guest:
            return None

        return Guest(**guest[0])
    
    def create_guest(self, guest: Guest) -> Guest:
        if self.get_guest(email=guest.email):
            raise ValueError("Guest already exists")
        
        column_model = self._get_column_model(guest=guest)
        self._db.insert_get(self._table, column_model)

        return guest
        
    def rsvp(self, guest: Guest, rsvp: str):
        if rsvp.upper() not in self._valid_rsvp:
            raise ValueError("Invalid RSVP value")

        guest.rsvp = rsvp
        guest: Dict = guest.to_dict()

        self._db.update(
            self._table,
            self._get_column_model(guest=guest)
        )
