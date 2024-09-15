from sqlalchemy import Column, String, Integer, Float, DateTime
from app.database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    subtype = Column(String)
    reading = Column(Integer)
    location = Column(String)
    timestamp = Column(DateTime)
