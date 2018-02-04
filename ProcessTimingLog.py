from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# CONFIGURATION
SQL_DATABASE = 'sqlite:///data/timing.db'

engine = create_engine(SQL_DATABASE, echo = True)
Base = declarative_base()

Base.metadata.create_all(engine)
