from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


Session = scoped_session(sessionmaker())
Base = declarative_base()


def bind_engine(engine, create_all=False):
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    if create_all is True:
        Base.metadata.create_all(engine)
