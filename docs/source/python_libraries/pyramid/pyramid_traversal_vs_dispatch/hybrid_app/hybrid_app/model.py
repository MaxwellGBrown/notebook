from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Unicode
from sqlalchemy.orm import scoped_session, sessionmaker, relationship


Session = scoped_session(sessionmaker())
Base = declarative_base()


def try_commit():
    try:
        Session.commit()
    except:
        Session.rollback()


def bind_engine(engine, create_all=False):
    """ binds engine to Session & Base.metadata """
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    if create_all is True:
        Base.metadata.create_all(engine)


# class RootFactory(object):
#     __name__ = None
#     __parent__ = None
# 
#     def __init__(self, request):
#         print("RootFactory.__init__")
#         self.request = request
# 
#     def __getitem__(self, key):
#         print('RootFactory["{}"]'.format(key))
#         if key == "foo_tree":
#             return FooFactory(parent=self)
#         else:
#             raise KeyError()
# 
#     def __repr__(self):
#         return 'RootFactory(__name__={}, __parent__={})'\
#                 .format(self.__name__.__repr__(), self.__parent__)


class FooFactory(object):
    __acl__ = list()
    __name__ = None
    __parent__ = None

    def __init__(self, *args):
        pass

    def __getitem__(self, key):
        try:
            foo =  Session.query(Foo).filter_by(foo_name=key).one()
            print('FooFactory["{}"] => {}'.format(key, foo.__repr__()))
            return foo
        except:
            print('FooFactory["{}"] => KeyError; FooFactory is context.'
                    .format(key))
            raise KeyError()

    def __repr__(self):
        return 'FooFactory(__name__="{}", __parent__={})'.format(
                self.__name__, self.__parent__.__repr__())

    def children(self):
        return Session.query(Foo).all()


class Foo(Base):
    __acl__ = list()

    @property
    def __name__(self):
        return self.foo_name

    @property
    def __parent__(self):
        return FooFactory()

    __tablename__ = "foo"

    foo_name = Column(Unicode(50), primary_key=True, index=True)

    def __getitem__(self, key):
        kwargs = {"foo_name": self.foo_name, "bar_name": key}
        try:
            bar = Session.query(Bar).filter_by(**kwargs).one()
            print(self.__repr__() + "[\"" + key + "\"] => " + bar.__repr__())
            return bar
        except:
            print('{0}["{1}"] => KeyError: {0} is context.'.format(
                self.__repr__(), key))
            raise KeyError()

    def __repr__(self):
        return 'Foo(foo_name="{}")'.format(self.foo_name)

    def children(self):
        for child in self.bars:
            yield child


class Bar(Base):
    __acl__ = list()

    @property
    def __name__(self):
        return self.bar_name

    @property
    def __parent__(self):
        return self.foo

    __tablename__ = "bar"

    bar_name = Column(Unicode(50), primary_key=True, index=True)

    foo = relationship("Foo", backref='bars')
    foo_name = Column(Unicode(50), ForeignKey("foo.foo_name"), nullable=False,
            primary_key=True, index=True)

    def __getitem__(self, key):
        kwargs = {
                "foo_name": self.foo_name,
                "bar_name": self.bar_name,
                "baz_name": key,
                }
        try:
            baz = Session.query(Baz).filter_by(**kwargs).one()
            print('{}["{}"]'.format(self.__repr__(), key))
            return baz
        except:
            print('{0}["{1}"] => KeyError; {0} is context.'.format(
                self.__repr__(), key))
            raise KeyError()

    def __repr__(self):
        return 'Bar(foo_name="{}", bar_name="{}")'.format(self.foo_name,
                self.bar_name)

    def children(self):
        for child in self.bazs:
            yield child



class Baz(Base):
    __acl__ = list()

    @property
    def __name__(self):
        return self.baz_name

    @property
    def __parent__(self):
        return self.bar

    __tablename__ = "baz"

    baz_name = Column(Unicode(50), primary_key=True, index=True)

    foo_name = Column(Unicode(50), ForeignKey("bar.foo_name"), nullable=False,
            primary_key=True, index=True)
    bar_name = Column(Unicode(50), ForeignKey("bar.bar_name"), nullable=False,
            primary_key=True, index=True)

    primaryjoin = "and_(Baz.foo_name==Bar.foo_name, "\
            "Baz.bar_name==Bar.bar_name)"
    bar = relationship("Bar", primaryjoin=primaryjoin, backref='bazs')

    def __getitem__(self, key):
        kwargs = {
                "foo_name": self.foo_name,
                "bar_name": self.bar_name,
                "baz_name": self.baz_name,
                "qux_name": key,
                }
        try:
            qux = Session.query(Qux).filter_by(**kwargs).one()
            print('{}["{}"]'.format(self.__repr__(), key))
            return qux
        except:
            print('{0}["{1}"] => KeyError; {0} is context'.format(
                self.__repr__(), key))
            raise KeyError()

    def __repr__(self):
        return 'Baz(foo_name="{}", bar_name="{}", baz_name="{}")'.format(
                self.foo_name, self.bar_name, self.baz_name)

    def children(self):
        for qux in self.quxs:
            yield qux


class Qux(Base):
    __acl__ = list()

    @property
    def __name__(self):
        return self.qux_name

    @property
    def __parent__(self):
        return self.baz

    __tablename__ = "qux"

    qux_name = Column(Unicode(50), primary_key=True, index=True)

    foo_name = Column(Unicode(50), ForeignKey("baz.foo_name"), nullable=False,
            primary_key=True, index=True)
    bar_name = Column(Unicode(50), ForeignKey("baz.bar_name"), nullable=False,
            primary_key=True, index=True)
    baz_name = Column(Unicode(50), ForeignKey("baz.baz_name"), nullable=False,
            primary_key=True, index=True)

    primaryjoin = "and_("\
            "Qux.foo_name==Baz.foo_name,"\
            "Qux.bar_name==Baz.bar_name,"\
            "Qux.baz_name==Baz.baz_name,"\
            ")"

    baz = relationship("Baz", primaryjoin=primaryjoin, backref="quxs",
            foreign_keys=[foo_name, bar_name, baz_name])

    # This resource is a "leaf-resource": it has no children
    # def __getitem__(self, key):
    #     pass

    def __repr__(self):
        return 'Qux(foo_name="{}", bar_name="{}", baz_name="{}", '\
                'qux_name="{}")'.format(self.foo_name, self.bar_name,
                        self.baz_name, self.qux_name)

    def children(self):
        return list()
