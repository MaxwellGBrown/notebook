====================
Dependancy Injection
====================

*How would you program without conditionals?*

Dependancy Injection is a tenant of Object Oriented Programming, in which an object/function is passed as an argument to a function to handle differing logics. This way, different logics don't have to live inside the code responsible for handling data. 

A Basic Example
---------------

In this example, there's a function that is leveraging Dependancy Injection.

.. code-block:: python

    # Probably Bad
    def alphabet(backwards=False, every_other=True):
        string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if backwards is True:
            string = string[::-1]
        if every_other is True:
            string = string[::2]
        return string

    # Dependancy Injection
    def alphabet(injected_dependancy):
        string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return injected_dependancy(string)

    def backwards(string):
        return string[::-1]

    def every_other(string):
        return string[::2]

    def backwards_every_other(string):
        return string[::-2]


To "inject a dependancy" to the alphabet, you'd pass a function in as
``injected_dependancy`` that handles the alphabet string.

Instead of adding more and more code into the alphabet function and adding more things to account for when calling the function, separating the logic outside of the function into other objects/functions makes for cleaner code and easier expandable code.


Autoloading New Dependancies
----------------------------

It's pretty easy to set up a Dependancy Injection where classes/functions
intended for injection are auto-loaded in to a dictionary where their __name__
is the key to the object.

.. code-block:: python

    import inspect
    import dependancies  # this is the module w/ the dependancies
    from dependancies import BaseDependancy  # all dependancies inherit this

    dependancy_injection_options = dict()
    for name, cls in inspect.get_members(dependancies):
        if inspect.isclass(cls):
            if issubclass(cls, BaseDependancy):
                if name == "BaseDependancy":
                    continue  # don't need to include the unimplemented base
                dependancy_injection_options[name] = cls


This creates a dictionary of all the classes that inherit ``BaseDependancy``, chich lays out the class definition of how any injected dependancies should operate at a minimum. 

Beyond that, any user defined dependancies work as a middleware and give the user the freedom to define any type of dependancy they desire.
