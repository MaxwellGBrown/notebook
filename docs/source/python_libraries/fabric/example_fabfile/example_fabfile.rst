.. _example_fabfile:

===================
Using fab & fabfile
===================

``fabric`` was meant to be used in conjuction with the ``fab`` command line tool. The ``fab`` command line tool looks to ``fabfile.py`` or a directory with ``__init__.py`` and imports for defined functions and uses them to work on remote hosts.

Below is an example ``fabfile.py``:

.. literalinclude:: fabfile.py
    :language: python
    :caption: An example fabfile.py

Although this ``fabfile`` is trivial, it can provide a good enough example to explain what fab was made for.

In the ``env.hosts`` list, we've supplied the hosts which these commands will be run on by default. At the command line, we run

::

    $ fab get_hostname
   
and it makes an SSH connection to each of the env.hosts and does ``run("hostname")``. 

~~~~~~~~
fab args
~~~~~~~~

``make_blank_file()`` provides an opportunity to show how function arguments work with ``fab``

::

     $ fab make_blank_file 
     $ fab make_blank_file:blank_file.txt
     $ fab make_blank_file:file_name=blank_file.txt
     
Note that all three are functionally equivalent. The 2nd option shows how to provide positional arguments, and the 3rd shows keword arguments.


~~~~~~~~~~~~~~~~~~~~~~~~~~
Two functions, one command 
~~~~~~~~~~~~~~~~~~~~~~~~~~

We can also combine fab commands into the one command line command

::

    $ fab get_hostname make_blank_file

This will cycle through ``env.hosts`` and do each command accordingly.

You can also call your own high-level fab functions in other fab functions!

::

   $ fab do_both

``$ fab do_both()`` is functionally equivalent to ``$ fab get_hostname make_blank_file``, but it's defined within our fab file.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Command line arguments for fab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``env`` object in the ``fabfile`` can be overwritten by arguments at the command line. Below is an example of how to override ``env.hosts``.

::

  $ fab -H localhost do_both

The ``-H`` flag means host. Use ``$ fab --help`` to show the different arguments that can be supplied.
