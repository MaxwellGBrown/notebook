from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool, NullPool
import pytest


# Session = sessionmaker()
Session = scoped_session(sessionmaker())  # scoped_session test
engine = create_engine("sqlite:///:memory:", poolclass=QueuePool)


@pytest.fixture(scope="module")
def database_head(request):
    Base.metadata.create_all(engine)


@pytest.fixture(scope="function")
def rollback(request, database_head):
    connection = engine.connect()
    transaction = connection.begin()
    # session = Session(bind=connection)
    Session.configure(bind=connection)  # scoped_session test

    def revert_changes():
        # session.close()
        Session.remove()  # scoped_session test; use instead of session.close()
        transaction.rollback()
        connection.close()

    request.addfinalizer(revert_changes)
    # return session
    return Session


@pytest.mark.usefixtures("rollback")
class TestRollbackFixtureSuite(object):

    def test1(self, rollback):
        session = rollback

        count = session.query(Foo).count()
        assert count == 0  # assert rollback happened

        session.add(Foo())
        session.commit()
        count = session.query(Foo).count()
        assert count == 1

    def test2(self, rollback):
        session = rollback

        count = session.query(Foo).count()
        assert count == 0  # assert rollback happened

        session.add(Foo())
        session.add(Foo())
        session.commit()

        count = session.query(Foo).count()
        assert count == 2


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer


Base = declarative_base()


class Foo(Base):
    __tablename__ = "foo"

    foo_id = Column(Integer, primary_key=True, autoincrement=True)
