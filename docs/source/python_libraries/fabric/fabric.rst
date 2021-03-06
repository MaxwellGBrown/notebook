.. _fabric:

======
fabric
======

.. warning::

   As of Mar 21, 2016 fabric has not yet been ported to Python 3!

``fabric`` is a Python (2.5-2.7) library for streamlining SSH for application deployment or system admin tasks.  It provides a basic suite of commands for local or remote shell commands.


**Examples**

.. toctree::
  :maxdepth: 1

  example_fabfile/example_fabfile
  programming_with_fabric/programming_with_fabric



Typical use involves creating a ``fabfile`` and executing commands in that file by using the ``fab`` command-line tool. 


------------------------------
A small, yet complete, fabfile
------------------------------

.. code-block:: python
    :caption: A simple fabfile.py

    from fabric.api import run

    def host_name():
        run('hostname')

When ``host_name`` is run using ``fab``...

::

    $ fab host_name
    [localhost] run: hostname
    [localhost] out: lebron
