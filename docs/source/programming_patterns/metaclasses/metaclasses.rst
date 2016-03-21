.. _python_metaclasses:

Metaclasses in Python
=====================

.. note:: 
  Metaclasses are deeper magic than 99% of users should ever worry about. If you wonder whether you need them, you don’t (the people who actually need them know with certainty that they need them, and don’t need an explanation about why).

  – Tim Peters (Python God & author of *The Zen of Python*)

Metaclassing is a seemingly complex idea where ``Class`` objects are programmatically defined. 

I use the words *seemingly* because, while the very practice of metaclassing dances around the dark edges of python, and the practice is rarely needed, it's really straightforward once understood. 

This page has been adapted from the (very helpful) `A Primer On Python Metaclasses <https://jakevdp.github.io/blog/2012/12/01/a-primer-on-python-metaclasses/>`_

Before diving in, the below glossary will establish a few terms:

.. _metaclass:

**metaclass**
  *a class that instantiates classes*

.. _metafunction:

**metafunciton**
  *a function that instantiates classes*


Understanding Type
------------------

python's peculiar built-in ``type`` can be used to find the type of an object.

::

  >>>type(1)
  <type 'int'>

But it's dark magic expands much further than type discovery. 

Technically, every defined class in python is of class ``type``.

::

  >>>class Foo(object):
  ...    pass
  ...
  >>>type(Foo)
  <type 'type'>

This just scratches the surface of the deep pit of complexity that is ``type``. 

``type``'s true form is as **the** metaclass_ in python.


Actually Defining Classes
-------------------------

So, if ``type`` is actually a metaclass then how does that all work?

Think about how classes are traditionally defined...

::

  class Foo(object):
      i = 4

  class Bar(Foo):
      def get_i(self):
          return self.i

This is a very basic parent-child relationship between two classes.

Using ``type`` as a metaclass these classes can be created like so:

::

  Foo = type('Foo', (), dict(i=4))

  Bar = type('Bar', (Foo,), dict(get_i = lambda self: self.i))


This is the breakdown of how ``type`` is used as a metaclass

**type(name, bases, dct)**
  *name*
    the ``__name__`` of the class to be constructed
  *bases*
    a tuple of the parent classes
  *dct*
    a ``dict`` of attributes & methods of the constructed class


Defining New Metaclasses
------------------------

Again: ``type`` is **the** metaclass in python.

So, to define a *new* metaclass, ``type`` just needs to be inherited!


.. code-block:: python 

  class Meta(type):
  
      @classmethod
      def __prepare__(metaclass, name, parents, **kwargs):
          return dict(kwargs) 

      def __new__(metaclass, name, parents, namespace, **kwargs):
          return super().__new__(metaclass, name, parents, namespace)

      def __init__(cls, name, parents, namespace, **kwargs):
          super().__init__(name, parents, namesapce) 

      def __call__(cls, *args, **kwargs):
          return super().__call__(*args, **kwargs)

While ``Meta`` has 4 different methods defined, not all of them are required to be overridden. 

Now the metaclass can be used to define classes!

::

  Foo = Meta('Bar', (,), dict(foo='bar'))
  
Inheriting a Metaclass
----------------------

Sure, calling a metaclass like calling ``type`` is the "standard" way of using metaclasses.

But if we're going to define our own metaclasses (instead of programmatically) then using ``type`` isn't very readable.

So, we can manipulate the ``class`` builtin to define that a class is constructed from a metaclass!

.. code-block:: python

   class Foo(object, metaclass=Meta):
       pass

It's as easy as that!

just adding the keyword argument ``metaclass`` to the builtin ``class`` definition declares a metaclass constructor for that class. 

.. note::

   In python 2.x, the ``class`` builtin does not accept the metaclass keyword argument, or any keyword arguments.

   To define a class as inheriting a metaclass, it's must be done with the ``__metaclass__`` class attribute.

   .. 
     
      class Foo(object):
          __metaclass__ = Meta

   Also, the use of ``__prepare__`` and ``**kwargs`` for metaclasses is not implemented in python2.


The Metaclass Methods
---------------------

Okay, so a metaclass can have those 4 methods (``__prepare__``, ``__new__``, ``__init__`` and ``__call__``). But what do they mean and how do they interact?

Truthfully, most metaclassing can be done with just ``__new__``: this is right before the defined class is actually created with python's scope, and allows the opportunity to run script to change/setup/override different things in the class definitoin before the class is obstantiated.

However, there's no harm in overriding all 4 of the methods used in metaclassing! 

Lets dive in to the 4 methods and how they interact:

__prepare__
+++++++++++

::
  
  class Meta(type):

      @classmethod
      def __prepare__(metaclass, name, parents, **kwargs):
          return dict(kwargs) 
      ...

  class Foo(object, metaclass=Meta, foo='bar'):
      pass


Any other keyword arguments passed after ``metaclass`` are sent as ``**kwargs`` to ``__prepare__`` which are then passed as the ``**kwargs`` to ``__new__``.In the above example, ``**kwargs={'foo':'bar'}``.


__new__
++++++++

::

  class Meta(type):
      ...
      def __new__(metaclass, name, parents, namespace, **kwargs):
          return super().__new__(metaclass, name, parents, namespace)
      ... 

  class Foo(object, metaclass=Meta, foo='bar'):
      i = 1

The class attributes & methods in the new class are passed as a dictionary to the 4th arg to ``__new__``  (which is titled ``namespace`` in this example). So in the above example ``namespace = {'i': 1}``.

The ``**kwargs`` passed to ``__new__`` is the dict that is returned by ``__prepare__``. Note that ``__prepare__`` can actually return whatever it wants, and that it just needs to be handled in ``__new__``.

Since ``__new__`` occurs before the class has been instantiated, the 1st argumetn (``metaclass``) is essentially an empty class object. Nothing in the namespace dictionary has been attributed to the class (yet).

__init__
++++++++

::
 
  class Meta(type):
      ...
      def __init__(cls, name, parents, namespace, **kwargs):
          super().__init__(name, parents, namesapce) 
      ...


  class Foo(object, metaclass=Meta, foo='bar'):
      i = 1

Operationally, ``__init__`` works much the same as ``__new__`` when metaclassing.

However, ``__init__`` takes place *after* class instantiation unlike ``__new__`` which takes place *before*. 

So, in this example, ``__init__``'s 1st argument (``cls``) would have this value: ``cls.i = 1``.

``__init__``'s kwargs are gathered from ``__prepare__`` and are ``**kwargs = {'foo':'bar'}``.

Lastly, ``__init__`` uses the namespace dict that ``__new__`` used

Again, this doesn't provide much of an operational difference between the two: it's "most best" to handle most metaclassing at the ``__new__`` level

__call__
++++++++

::

  class Meta(type):
      ...
      def __call__(cls, *args, **kwargs):
          return super().__call__(*args, **kwargs)

Lastly, ``__call__`` refers to when the metaclass is called to create an instance of a class. It acts as a middleware which can intercept the ``*args`` and ``**kwargs`` before passing them to the classes ``__init__``.  


Conclusion
----------

Again, metaclassing isn't needed in 99% of programming cases, and a lot of instances where it can be used are still not the cleanest solutions. However, knowing how to use metaclasses is important so that when it *is* needed it can be used.

If anything should be remembered from this rant, let it be known that...

**type** is *waaaayyy* more than a function to determine a class's constructor.

``type`` is **the** metaclass!


.. _metaclass_summary:

Summary
-------

Here's the quick and dirty!


.. code-block:: python 

  class Meta(type):
      """
      This is the metaclass!
      """
  
      @classmethod
      def __prepare__(metaclass, name, parents, **kwargs):
          return dict(kwargs) 

      def __new__(metaclass, name, parents, namespace, **kwargs):
          return super().__new__(metaclass, name, parents, namespace)

      def __init__(cls, name, parents, namespace, **kwargs):
          # cls has all of the attributes/methods from __new__'s namespace
          super().__init__(name, parents, namesapce) 

      def __call__(cls, *args, **kwargs):
          return super().__call__(*args, **kwargs)


  class Foo(object, metaclass=Meta, foo="bar"):  # **kwargs = {'foo': 'bar'}
      hello = "World"  # namespace = {'hello': "World"}

      def __init__(self, a, b='B'):  # __call__ *args & **kwargs 
          pass
