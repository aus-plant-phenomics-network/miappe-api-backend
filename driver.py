import uuid

from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import create_session

from miappe.model import Base, Device


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


engine = create_engine("sqlite:///db.sqlite", echo=True)
Base.metadata.create_all(engine)

session = create_session(engine)

random_id = uuid.uuid4()
myDevice = Device(name="myDevice", device_type_id=random_id)
session.add(myDevice)
# session.commit()
