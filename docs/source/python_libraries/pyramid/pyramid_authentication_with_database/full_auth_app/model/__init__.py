import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = None
Base = declarative_base()
metadata = Base.metadata
Session = scoped_session(sessionmaker())
