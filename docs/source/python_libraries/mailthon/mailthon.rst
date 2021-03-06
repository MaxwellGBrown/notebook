.. _mailthon:

========
mailthon
========

mailthon is an SMTP library that reflects the simplicty of the requets library.

**Examples**

.. toctree::
   :maxdepth: 1
   
   mailthon_enclosure/mailthon_enclosure
   mailthon_headers/mailthon_headers
   mailthon_middleware/mailthon_middleware
   mailthon_and_email/mailthon_and_email
     


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
