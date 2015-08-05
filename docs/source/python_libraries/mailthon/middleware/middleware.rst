==========
middleware
==========

``mailthon`` allows us to plug middleware into our SMTP connection so that we can interact with other features of our SMTP server. It's important to note that the middleware can only interact with with the SMTP server connection object, and nothing else. Any middleware made will depend solely on the different commands and interactions the SMTP server provides. 

-----------------
Middleware Basics
-----------------

The minimum requirements for a working ``Middleware`` is to override ``Middleware.__call__(self, conn)``. This method is supplied an ``smtplib.SMTP`` connection object before an email has been passed to the SMTP server.


::

    import mailthon
    from mailthon.middleware import Middleware    
    
    class HelpMiddlware(Middleware):
        
        def __call__(self, conn):
            response = conn.docmd("HELP")  # conn is an smtplib.SMTP connection
            print "SMTP servers response from HELP:\n\"{}\"".format(response)
    
    postman = mailthon.postman("gmail.com")
    postman.use(HelpMiddlware())



As shown above, we attach our new middleware as an obstantiate object to ``Postman`` using ``Postman.use()``. Alternatively you can assign middlewares to a ``Postman`` on obstantiation in a list.

Note that ``mailthon.postman`` is a function that obstantiates a ``Postman`` with ``TLS`` and ``Auth`` already attached and not the initialization of a ``Postman`` object itself.

~~~~~~~~~~~~~~~~~~~~~~~
More about Auth and TLS
~~~~~~~~~~~~~~~~~~~~~~~
``mailthon`` comes pre-packaged with ``Auth``, a middleware for authenticating users to an SMTP server, and ``TLS`` a middleware that implements TLS connections if possible.
