import datetime
import ormar
from db import database, metadata




class Image(ormar.Model):
    class Meta:
        tablename = "inbox"
        metadata = metadata
        database = database
    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=36)
    registration_date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)

