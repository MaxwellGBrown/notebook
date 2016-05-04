from hashlib import sha1
import os

from pyramid.security import unauthenticated_userid, Allow, Deny, Everyone,\
        Authenticated
from sqlalchemy import Column, Integer, Unicode, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from full_auth_app.model import Base, Session


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(Unicode(32), unique=True)
    _password = Column('password', Unicode(255))  # @property = .password

    membership = relationship("GroupMember")

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, password):
        hashed_password = User.hash_password(password)
        self._password = hashed_password

    @staticmethod
    def hash_password(password):
        salt = sha1(os.urandom(60))
        salted_pwd = password + salt.hexdigest()
        sha1_hash = sha1(salted_pwd.encode("UTF-8"))
        hashed_password = salt.hexdigest() + sha1_hash.hexdigest()
        return hashed_password

    def validate(self, password):
        combined_password = password + self.password[:40]
        hashed_password = sha1(combined_password.encode("UTF-8"))
        passwords_match = self.password[40:] == hashed_password.hexdigest()
        return passwords_match

    def get_groups(self):
        return list([gm.group for gm in self.membership])


class Group(Base):
    __tablename__ = "group"

    @property
    def __acl__(self):
        perms = list()
        if self.private is True:
            perms.append((Allow, "group:{}".format(self.groupname), "view"))
            perms.append((Deny, Everyone, "view"))
        else:
            perms.append((Allow, Authenticated, "view"))
        return perms

    id = Column(Integer, autoincrement=True, primary_key=True)
    groupname = Column(Unicode(64), unique=True)
    private = Column(Boolean(), default=False)

    members = relationship("GroupMember")

    def get_members(self):
        return list([m.user for m in self.members])

    def is_admin(self, user):
        """ return True if user is admin of group, False otherwise """
        for member in self.members:
            if member.user is user:
                return member.is_admin
        else:
            return False

    def add_member(self, user, **kwargs):
        kwargs['user'] = user
        kwargs['group'] = self
        new_gm = GroupMember(**kwargs)
        Session.add(new_gm)
        try:
            Session.commit()
        except:
            Session.rollback()

    def remove_member(self, user):
        for member in self.members:
            if member.user is user:
                Session.delete(member)
                try:
                    Session.commit()
                except:
                    Session.rollback()



class GroupMember(Base):
    """ a many-to-many w/ more properties between User & Group"""
    __tablename__ = "user_group"
    # __table_args__ = (
    #         PrimaryKeyConstraint("user_id", "group_id", name="groupmember_pk"),
    #         )

    user = relationship("User")
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    group = relationship("Group")
    group_id = Column(Integer, ForeignKey("group.id"), primary_key=True)

    is_admin = Column(Boolean, default=False)


def find_user(username):
    """ attempt to find a User by User.username """
    return Session.query(User).filter_by(username=username).first()


def all_users():
    return Session.query(User).all()


def all_groups():
    return Session.query(Group).all()


def get_users(**kwargs):
    return Session.query(User).filter_by(**kwargs).all()


def get_groups(**kwargs):
    return Session.query(Group).filter_by(**kwargs).all()


def new_user(**kwargs):
    """ create and attempt to commit a new user """
    new_user = User(**kwargs)
    Session.add(new_user)
    try:
        Session.commit()
    except:
        Session.rollback()
    return new_user


def new_group(**kwargs):
    """ create and attempt to commit a new group """
    new_group = Group(**kwargs)
    Session.add(new_group)
    try:
        Session.commit()
    except:
        Session.rollback()
    return new_group


def get_user(request):
    """
    request.user - config.add_request_method(get_user, 'user', reify=True)
    """
    userid = unauthenticated_userid(request)
    user = Session.query(User).filter_by(id=userid).first()
    return user  # either a found User ORM object or None


def groupfinder(userid, request):
    """
    AuthTktAuthenticationPolicy(..., callback=groupfinder, ...)

    relies on request.user from ``get_user(request)``
    """
    if request.user is not None:
        perms = list()
        for group in request.user.get_groups():
            perms.append("group:{}".format(group.groupname))
        return perms
    else:
        return None
