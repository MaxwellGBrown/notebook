========
mailthon
========

mailthon is an SMTP library that reflects the simplicty of the requets library.

.. toctree::
    :maxdepth: 1
    
    examples/enclosure
    examples/headers
    examples/middleware
    examples/email_library 


----------
Quickstart
----------

::

    import mailthon

    headers = {
        "To": "janedoe@gmail.com",
        "From": "johndoe@gmail.com",
        "Subject": "Hello World",
        }
    plaintext = mailthon.enclosure.PlainText("Foo Bar") 
    enclosures = [plaintext]
    envelope = mailthon.envelope.Envelope(headers, enclosures)

    credentials = (
                "johndoe@gmail.com",  # email address
                "hunter2",  # password
                )
    postman = mailthon.postman(host="gmail.com", auth=credentials)

    response = postman.send(envelope)
    
    assert response.ok


Mailthon uses ``Postman`` as an smtp server connection, and ``Envelope`` to represent the email. 

An ``Envelope`` is composed of two parts: ``headers`` which represent the email headers, and ``enclosures`` which represent the email payload.

Lastly, after using ``Postman`` to send an email, it will return a ``Response`` which can be used to determine the outcome of sending the message.
