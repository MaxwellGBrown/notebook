from sqlalchemy import Column, Integer, Unicode

from database_app.models import Base, Session


class Contact(Base):
    """ an example ORM object """
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode)
    last_name = Column(Unicode)
    address = Column(Unicode)
