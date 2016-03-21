=======
pymongo
=======

pymongo is a package used to communicate with ``mongodb``.


``mongodb`` is a NoSQL database that stores dynamic-schema JSON-like objects.

----------------
Why use mongodb?
----------------

There's much debate about whether ``mongodb`` is worth implementing.

First off, if one intends to create any sort of relational database then DO NOT USE MONGODB.

Second, ``mongodb`` may seem flexible in that it's a non-schema'd database, but *real flexibility* comes from how easy it is to add features. If there's any sort of even remotely possible future feature that might benefit from a relational database then DO NOT USE MONGODB.

If the goal is to store arbitrary JSON pieces, then *maybe* ``mongodb`` is the right solution. (And, even then, ``PostgreSQL``'s ``hstore`` is probably a better solution).

So, now that that's out of the way... *how do you use mongodb?*


----------
Quickstart
----------

If one's looking to just get something light up & running, ``mongodb`` is quite easy to setup & get going!

This tutorial quickly breaks down `pymongo's basic tutorial <api.mongodb.org/python/current/tutorial.html>`_ with a little extra on spinning up a mongodb instance.

^^^^^^
mongod
^^^^^^

Firstly, one must have a ``mongodb`` server to run on. 

``mongodb`` is built to use multiple nodes & shard pieces, but it can run perfectly fine on the host machine as a single node if need be.

::

    # install mongodb
    sudo apt-get install mongodb

    # start the mongodb server   
    mongod --dbpath /data/db
    # or...
    sudo service mongodb start


.. note::

   to get mongodb to run exclusivly to requests inside the host, add ``--bind_ip 127.0.0.1`` to the ``mongod`` command.

^^^^^^^^^^^^^
using pymongo
^^^^^^^^^^^^^

``mongodb`` holds sub-databases within it's database. Within these databases, there are ``collections`` which are akin to a SQL table.

Below is a simple interaction using ``pymongo`` to create a collection, then write 1 record to it.

.. code-block:: python

  from pymongo import MongoClient

  client = MongoCliient('mongodb://localhost:27017/')

  db = client['example_database']
  collection = db['example_collection']

  record = {
      "text": "hello world",
      "foo": ["bar", "baz"],
  }
  collection.insert_one(record)

  returned_record = collection.find_one({"text": "hello world"})


