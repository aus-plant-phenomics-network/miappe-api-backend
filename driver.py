import uuid

from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import create_session

from miappe.model import Base, Device, Method, Vocabulary


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


engine = create_engine("sqlite:///db.sqlite", echo=True)
Base.metadata.create_all(engine)

session = create_session(engine)

camera = Vocabulary(name="camera", description="RGB Camera")
nikon_camera = Device(name="NIKON A1", description="NIKON A1", brand="NIKON")
sony_camera = Device(name="SONY S1", description="SONY A1", brand="SONY")
camera.device.append(nikon_camera)
camera.device.append(sony_camera)

mobile_phone = Vocabulary(name="mobile_phone", description="Mobile Phone")
apple_phone = Device(name="apple iphone", description="apple iphone", brand="apple")
mobile_phone.device.append(apple_phone)

taking_photo = Vocabulary(name="photo_capture", description="Method of taking pictures")
iphone_capture = Method(name="iphone_photo_capture", description="Taking photo using an iphone")
iphone_capture.device = apple_phone
taking_photo.method.append(iphone_capture)

session.add(camera)
session.add(mobile_phone)
session.add(taking_photo)
session.commit()