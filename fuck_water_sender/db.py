from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from fuck_water_sender import constants as C

Base = declarative_base()
engine = create_engine(C.DB_URL, connect_args={'timeout': 15})
Session = sessionmaker(bind=engine)
session = Session()


class Metric(Base):

    __tablename__ = 'metric'

    TIMESTAMP = Column(Integer, primary_key=True)
    COD = Column(Float)
    NH3 = Column(Float)
    TP = Column(Float)
    TN = Column(Float)
    SS = Column(Float)

    sended = Column(Boolean, default=False)

    def __repr__(self):
        return '<Metric {}>'.format(self.TIMESTAMP)
