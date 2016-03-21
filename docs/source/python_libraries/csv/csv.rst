.. _csv:

===
csv
===

``csv`` is an included python module that reads .csv files!

For more in-depth description of the ``csv`` module, visit `the official docs <https://docs.python.org/3/library/csv.html>`__.

----------
Quickstart
----------

``csv`` provides the means to both easily read and write a csv file.

Both of these exaples use the "Dictionary" versions of their Reader/Writer counterpart, because I like explicit better. But for different implementations there's a non-Dict Reader/Writer.

++++++++++++++
Reading a .csv
++++++++++++++

::

  from csv import DictReader

  with open('read_example.csv', 'r') as csv_file:
      reader = DictReader(csv_file)

      for line_dict in reader:
          print(line_dict)

For more on ``DictReader`` & the other "Reader" objects check the `official docs entry for them <https://docs.python.org/3/library/csv.html#reader-objects>`__!

++++++++++++++
Writing a .csv
++++++++++++++

::

  from csv import DictWriter

  with open('write_example.csv', 'w') as csv_file:
      columns = ('foo', 'bar')
      writer = DictWriter(csv_file, fieldnames=columns)

      writer.writeheader()
      writer.writerow({'foo': 'Hello', 'bar': 'World'}) 


For more on ``DictReader`` & the other "Writer" objects `official docs entry for them <https://docs.python.org/3/library/csv.html#writer-objects>`__
