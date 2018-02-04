from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import Config as config

engine = create_engine(config.SQL_DATABASE, echo = True)
Base = declarative_base()


class Logfile(Base):
    __tablename__ = 'logfiles'

    id = Column(Integer, primary_key = True)
    filename = Column(String, nullable = False)


class SpillType(Base):
    __tablename__ = 'spill_types'

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    evtcode = Column(Integer, nullable = False)


class Spill(Base):
    __tablename__ = 'spills'

    id = Column(Integer, primary_key = True)
    spill_type_id = Column(Integer, ForeignKey('spill_types.id'), nullable = False)
    time_spillserver = Column(DateTime)
    time_fwd_near = Column(DateTime)
    time_rec_near = Column(DateTime)
    time_fwd_far = Column(DateTime)
    time_rec_far = Column(DateTime)


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
