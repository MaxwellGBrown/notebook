from hashlib import sha1
import os

from pyramid.security import unauthenticated_userid
from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.ext.hybrid import hybrid_property

from auth_app.model.meta import Base, Session


def auth_callback(user_id, request):
    """ returns list of all principals associated w/ user_id """
    user_id = unauthenticated_userid(request)
    if user_id is None:
        return None

    user = UserMgr.first(user_id=user_id)
    if user is not None:
        # ADD PRINCIPALS HERE
        return list()
    else:
        return None


def request_user(request):
    user_id = unauthenticated_userid(request)
    if user_id is not None:
        return UserMgr.one(user_id=user_id)
    else:
        return None



class UserMgr(object):

    commit = Session.commit

    @staticmethod
    def get(**kwargs):
        return Session.query(User).filter_by(**kwargs)

    @classmethod
    def first(cls, **kwargs):
        return cls.get(**kwargs).first()

    @classmethod
    def one(cls, **kwargs):
        try:
            return cls.get(**kwargs).one()
        except:
            return None

    @staticmethod
    def new(**kwargs):
        new_user = User(**kwargs)
        Session.add(new_user)
        print("new user: ", new_user)
        return new_user


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(Unicode(255), unique=True)
    _password = Column('password', Unicode(255), nullable=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, password):
        """ requires password is UTF-8 """
        salt = sha1(os.urandom(60))
        salted_pwd = password + salt.hexdigest()
        sha1_hash = sha1(salted_pwd.encode("UTF-8"))
        self._password = salt.hexdigest() + sha1_hash.hexdigest()

    def validate(self, password):
        combined_password = password + self.password[:40]
        hashed_password = sha1(combined_password.encode("UTF-8"))
        passwords_match = self.password[40:] == hashed_password.hexdigest()
        return passwords_match
