
from sqlalchemy import Column, Integer, Float, String, DateTime
from Database.database import Base


class ObservationMeteo(Base):
    __tablename__ = "observations_meteo"

    id = Column(Integer, primary_key=True, index=True)

    station = Column(String, index=True)
    date_observation = Column(DateTime, index=True)

    temperature = Column(Float, nullable=True)
    pression = Column(Float, nullable=True)
    humidite = Column(Float, nullable=True)
    point_de_rosee = Column(Float, nullable=True)

    vent_moyen = Column(Float, nullable=True)
    vent_rafales = Column(Float, nullable=True)
    vent_direction = Column(Float, nullable=True)

    pluie_1h = Column(Float, nullable=True)
    pluie_3h = Column(Float, nullable=True)
