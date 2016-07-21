==============================
Unique Dictionary Combinations
==============================

``itertools`` packages a few strong "choice" tools. In particular, there's one
titled ``combinations`` which takes an iterable and a number of
options-per-combo and yields each combination of those items.

::

  >> pool = ["A", "B", "C"]
  >> for combo in itertools.combinations(pool, 2):
  >>    print(combo)

  ("A", "B")
  ("A", "C")
  ("B", "C")


How does one mimic this functionality with ``dict``?


-----------------
dict_combinations
-----------------

``dict_combinations`` is a generator that returns all the possible combinations
of each key's values (which is assumed to be an iterable). 


.. code-block:: python

  from collections import OrderedDict
  
  
  def dict_combinations(source_dict):
      """yield all combinations of a dictionaries values by key"""
      if len(source_dict) == 0:  # basis case
          yield {}
  
      else:
          # alter dict for next recursion
          this_dict = OrderedDict(source_dict)
          this_key = [k for k in this_dict.keys()][0]
          this_value = this_dict.pop(this_key)
  
          # get this_values' items
          if isinstance(this_value, list) or isinstance(this_value, set)\
                  or isinstance(this_value, tuple):
              values = tuple(this_value)
          else:
              values = tuple([v for v in this_value.values()])
  
          # generate all subcombinations of the value
          for value in values:
              for combo in dict_combinations(this_dict):
                  partial = OrderedDict()
                  partial[this_key] = value
                  partial.update(combo)
                  yield partial


``dict_combinations`` iterates through the values of each key and adds it to a
partially complete (``partial``) dictionary.

Then, using the remaining key/values, ``dict_combinations`` is called to yield
the next key's values, and so on until there are no more key/values left.

After a basis case is reached, each partial dictionary is yielded to the
previous recursion of ``dict_combinations``, where the partial dictionary is
``.update``-ed to include the other partials, until a complete combination is
built. 


.. note::
   Because ``dict_combinations`` is a recursive function, it is restrained by the typical restraints applied to recursive functions by python.


++++++++++++++
example output
++++++++++++++


::

    >>> x = OrderedDict()
    >>> A = x.setdefault('A', OrderedDict())
    >>> A['1'] = 'A1'
    >>> A['2'] = 'A2'
    >>> A['3'] = 'A3'
    >>> B = x.setdefault('B', list())
    >>> B.append("B1")
    >>> B.append("B2")
    >>> B.append("B3")
    >>> C = x.setdefault('C', OrderedDict())
    >>> C['Key1'] = "C1"
    >>> C['Key2'] = "C2"
    >>> for c in dict_combinations(x):
    >>>     print(c)

    OrderedDict([('A', 'A1'), ('B', 'B1'), ('C', 'C1')])
    OrderedDict([('A', 'A1'), ('B', 'B1'), ('C', 'C2')])
    OrderedDict([('A', 'A1'), ('B', 'B2'), ('C', 'C1')])
    OrderedDict([('A', 'A1'), ('B', 'B2'), ('C', 'C2')])
    OrderedDict([('A', 'A1'), ('B', 'B3'), ('C', 'C1')])
    OrderedDict([('A', 'A1'), ('B', 'B3'), ('C', 'C2')])
    OrderedDict([('A', 'A2'), ('B', 'B1'), ('C', 'C1')])
    OrderedDict([('A', 'A2'), ('B', 'B1'), ('C', 'C2')])
    OrderedDict([('A', 'A2'), ('B', 'B2'), ('C', 'C1')])
    OrderedDict([('A', 'A2'), ('B', 'B2'), ('C', 'C2')])
    OrderedDict([('A', 'A2'), ('B', 'B3'), ('C', 'C1')])
    OrderedDict([('A', 'A2'), ('B', 'B3'), ('C', 'C2')])
    OrderedDict([('A', 'A3'), ('B', 'B1'), ('C', 'C1')])
    OrderedDict([('A', 'A3'), ('B', 'B1'), ('C', 'C2')])
    OrderedDict([('A', 'A3'), ('B', 'B2'), ('C', 'C1')])
    OrderedDict([('A', 'A3'), ('B', 'B2'), ('C', 'C2')])
    OrderedDict([('A', 'A3'), ('B', 'B3'), ('C', 'C1')])
    OrderedDict([('A', 'A3'), ('B', 'B3'), ('C', 'C2')])
