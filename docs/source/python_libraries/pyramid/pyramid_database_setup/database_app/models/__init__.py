from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


Session = scoped_session(sessionmaker())
Base = declarative_base()


""" import objects as part of `` import database_app.models as app_model """
from database_app.models.contact import Contact


def bind_engine(engine, create_all=False):
    """ binds engine to Session & Base.metadata """
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    if create_all is True:
        Base.metadata.create_all(engine)
