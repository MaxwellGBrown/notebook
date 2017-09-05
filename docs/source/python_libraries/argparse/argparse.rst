.. _argparse:

========
argparse
========

`argparse <https://docs.python.org/3/library/argparse.html>`__ is a package used to parse command-line arguments. Use it to make command-line 

----------
Quickstart
----------

argparse at the highest level is a pretty straight-forward package. 

All you have to do is define an ``ArgumentParser``, add some arguments using ``ArgumentParser.add_argument()``, and then call ``ArgumentParser.parse_args()``. 

.. code-block:: python

  import argparse

  # A "script" should just be a way to call business logic modules!
  # Make them separate!
  import business_logic


  def main(**kwargs):
      business_logic.do_the_thing(**kwargs) 


  # Define the Parser at the module level for your script.
  parser = argparse.ArgumentParser(description="An example script!")
  parser.add_argument("argument1", type=int, help="the first arg!")
  parser.add_argument("--flag1", "-f1",
      dest="first_flag",
      action="store_true",
      default=False
  )


  if __name__ == "__main__":
      args = parser.parse_args()
      args_dict = vars(args)  # Namespace => dict conversion
      main(**args_dict)


---------
Resources
---------

* `ArgumentParser <https://docs.python.org/3/library/argparse.html#argumentparser-objects>`__
* `add_argument() <https://docs.python.org/3/library/argparse.html#the-add-argument-method>`__
* `add_argument's 'type' keyword <https://docs.python.org/3/library/argparse.html#type>`__
* `argparse.FileType <https://docs.python.org/3/library/argparse.html#filetype-objects>`__
* `Argument Groups <https://docs.python.org/3/library/argparse.html#argument-groups>`__
* `Sub-commands & Sub-parsers <https://docs.python.org/3/library/argparse.html#sub-commands>`__
* `setup.py entry_points for console scripts <http://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-console-scripts-entry-point>`__
