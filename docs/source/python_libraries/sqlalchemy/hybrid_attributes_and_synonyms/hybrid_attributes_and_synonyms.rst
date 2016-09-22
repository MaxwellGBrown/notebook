==============================
Hybrid Attributes and Synonyms
==============================

Sometimes accessing an ORM's column as a standard attribute isn't enough.

What if a column needs getters and setters? What if an ORM object wants to reference a column by a name different than it's attributes name?

SQLAlchemy provides two (well documented) ways to manipulate attributes: `hybrid attributes <http://docs.sqlalchemy.org/en/latest/orm/extensions/hybrid.html>`__ and `synonyms <http://docs.sqlalchemy.org/en/latest/orm/mapped_attributes.html#synonyms>`__.

When to use which?
------------------

Technically, ``synonym`` can do anything ``hybrid_attribute`` can. 

However, ``hybrid_attribute`` is more straigtforward to use in more complex situations, and represents what it's doing in a more-clear fashion.

**Synonym**

    For when you need a different attribute to represent an already existing attribute.

**Hybrid Attribute**

    For when you need to run queries based on manipulated column data, or when you need to provide a getter/setter for an ORM attribute.

Hybrid Attributes
-----------------

Hybrid attributes allow the definition of attributes that can be referenced in queries for objects.

.. code-block:: python

    from sqlalchemy import Column, Integer
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.hybrid import hybrid_property

    class Rectangle(Base):
        __tablename__ == "rectangle"

        id = Column(Integer, primary_key=True)
        width = Column(Integer, nullable=False)
        height = Column(Integer, nullable=False)

        @hybrid_property
        def area(self):
            return self.width * self.height


Using the above ``Rectangle`` model, we can run a query for all ``Rectangle`` objects based on their ``area`` hybrid attribute

.. code-block:: python

    >>> Session().query(Rectangle).filter_by(area > 10)
    SELECT rectangle.id AS rectangle_id, rectangle.width AS rectangle_width,
    rectangle.height AS rectangle_height
    FROM rectangle
    WHERE rectangle.width * rectangle.height > :param_1


Hybrid attributes also work very well for providing getter/setter attributes for other columns. 

.. code-block:: python

    from hashlib import sha1
    import os

    from sqlalchemy import Column, Integer, Unicode
    from sqlalchemy.ext.hybrid import hybrid_property


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


Synonyms
--------

Synonym provides another name for an already existing ORM attribute.

.. code-block:: python

    from sqlalchemy.ext.declarative import synonym

    class Foo(Base):
        __tablename__ = 'foo'

        id = Column(Integer, primary_key=True)
        bar = Column(String(50))

        baz = synonym("bar")


In this example, ``Foo.bar`` and ``Foo.baz`` are identical, and refer to the same value in the database (column "bar", since that's the column definition).

Synonym can also be used on descriptors to allow a differen nuanced access of other attributes.

.. code-block:: python

    from sqlalchemy.ext.declarative import synonym_for

    class Foo(Base):
        __tablename__ = "foo"

        id = Column(Integer, primary_key=True)
        _bar = Column(String(50))

        @synonym_for("bar")
        @property
        def baz(self):
            return self._bar

        @baz.setter
        def set_baz(self, value):
            self._bar = value

In the above example, the interface for ``Foo._bar`` would ideally be ``Foo.baz`` because _bar is a "private" (haha) attribute




