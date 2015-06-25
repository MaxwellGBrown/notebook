======
fabric
======

``fabric`` is a Python (2.5-2.7) library for streamlining SSH for application deployment or system admin tasks.  It provides a basic suite of commands for local or remote shell commands.


--------
Examples
--------

.. toctree::
  :maxdepth: 1
  :glob:

  examples/*



Typical use involves creating a ``fabfile`` and executing commands in that file by using the ``fab`` command-line tool. 


------------------------------
A small, yet complete, fabfile
------------------------------

::

    from fabric.api import run

    def host_name():
        run('hostname')

When ``host_name`` is run using ``fab``...

::

    $ fab host_name
    [localhost] run: hostname
    [localhost] out: lebron
