from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import Config as config

engine = create_engine(config.SQL_DATABASE, echo = config.DEBUG)
Base = declarative_base()

Session = sessionmaker(bind = engine)
session = Session()

class Logfile(Base):
    __tablename__ = 'logfiles'

    id = Column(Integer, primary_key = True)
    filename = Column(String, nullable = False, unique = True)

class Detector(Base):
    __tablename__ = 'detectors'
    
    id = Column(Integer, primary_key = True)
    fullname  = Column(String, nullable = False)
    shortname = Column(String, nullable = False)

class SpillType(Base):
    __tablename__ = 'spill_types'

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    evtcode = Column(Integer, nullable = False)

class Spill(Base):
    __tablename__ = 'spills'

    id = Column(Integer, primary_key = True)
    spill_type_id = Column(Integer, ForeignKey('spill_types.id'), nullable = False)
    time = Column(Integer)

class SpillReceived(Base):
    __tablename__ = 'spillsReceived'
    
    id = Column(Integer, primary_key = True)
    time_spillserver = Column(Integer, ForeignKey('spills.time'))
    detector_id = Column(Integer, ForeignKey('detectors.id'))
    partition = Column(Integer)
    time = Column(Integer)

class SpillForwarded(Base):
    __tablename__ = 'spillsForwarded'
    
    id = Column(Integer, primary_key = True)
    spill_type_id = Column(Integer, ForeignKey('spill_types.id'), nullable = False)
    time_spillserver = Column(Integer, ForeignKey('spills.time'))
    detector_id = Column(Integer, ForeignKey('detectors.id'))
    timeBegin = Column(Integer)
    timeEnd = Column(Integer)
    

class Heartbeat(Base):
    __tablename__ = 'heartbeats'

    id = Column(Integer, primary_key = True)
    time = Column(DateTime)
    app = Column(String)

class TDU(Base):
    __tablename__ = 'tdus'

    id = Column(Integer, primary_key = True)
    hostname = Column(String)

class TCR(Base):
    __tablename__ = 'tcrs'

    id = Column(Integer, primary_key = True)
    tdu_id = Column(Integer, ForeignKey('tdus.id'), nullable = False)
    delta = Column(Integer, nullable = False)

Base.metadata.create_all(engine)


# Set up static tables
if session.query(Detector).filter(Detector.id == 1).first() == None:
    session.add(Detector(id = 1, fullname = 'NearDet', shortname = 'ND'))
    
if session.query(Detector).filter(Detector.id == 2).first() == None:
    session.add(Detector(id = 2, fullname = 'FarDet',  shortname = 'FD'))
