"""
bootstrap_writer.py

While there are a few projects for turning .rst into bootstrap html, I want to
have custom control over how my application does it.

bootstrap-rst
-------------
https://github.com/rougier/bootstrap-rst

NOTE:
    see this for how to interact w/ docutils writers!
https://github.com/rougier/bootstrap-rst/blob/master/bootstrap.py


basicstrap
----------
https://github.com/tell-k/sphinxjp.themes.basicstrap/tree/master/src
"""

# To use a custom writer, you'll also probably have to define a special builder
# class that specifically uses that builder.
