====================================
MaxwellGBrown's Programming Notebook
====================================

Hello!

To build and view the Sphinx doc Notebook do the following:

::

    python view_docs.py

Please note you'll need to have sphinx installed to view them!


----------------
Easy Bash Access
----------------

Below is a script that curcumvents having to run ``view_docs.py`` to view Notebook.

::

  #! /bin/bash 
  <Notebook_virtualenv_path>/bin/python <Notebook_dir_path>/view_docs.py "$@"


Add this script to ``~/bin/``, name the script ``notebook``, and then build the docs like this:

::

  user@host:~$ notebook
