"""
mailthon example

===============
4-Middleware.py
===============

mailthon lets you plug middlewares into your postman (smtp connection). This
example explores how that might be done.
"""

smtp = str(raw_input("mail server: "))
email = str(raw_input("email address: "))
password = str(raw_input("password for {}: ".format(email)))
auth = (email, password)


import mailthon


class example_middleware(mailthon.middleware.Middleware):

    def __call__(self, conn):
        """This is what is called by Postman to activate the middleware.

        conn is an obstantiated smtplib.SMTP connection that has already
        done the helo command.

        This middleware will run HELP on the SMTP server which will give us a
        list of commands supported by the server.
        """
        response = conn.docmd("HELP")
        print "SMTP servers response from HELP:\n\"{}\"".format(response)


# Note that mailthon.postman is actually a call to the function
# mailthon.api.postman which returns an obstantiate mailthon.postman.Postman
# that already has the auth and TLS middlewares activated.
postman = mailthon.postman(smtp, auth=(email, password))

# we can plug our new middleware in using Postman.use() on an obstantiated
# middleware
postman.use(example_middleware())

postman.send(mailthon.email(sender=email, receivers=[email],
    subject="4-Middleware.py", content="4-Middleware.py"))
