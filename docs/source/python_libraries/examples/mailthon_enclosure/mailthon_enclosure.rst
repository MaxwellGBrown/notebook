===================
Mailthon Enclosures
===================

------------------
mailthon.enclosure
------------------ 

An ``Enclosure`` is a mailthon object that represents the payload of the email. ``Enclosure`` objects are passed to the ``Envelope`` in the order of appearance in a multipart message. mailthon comes packaged with four enclosures (``PlainText``, ``HTML``, ``Binary``, and ``Attachment``) which are all derived from the base ``Enclosure`` class. 

~~~~~~~~~~~~~~~~~~~
Basic Enclosure Use
~~~~~~~~~~~~~~~~~~~

Use enclosures to create the payload of the email. Most all emails are comprised of PlainText at least, sometimes both PlainText and HTML.

::

    import mailthon
    from mailthon.enclosure import PlainText, HTML

    plaintext = PlainText("Hello World", encoding='utf-8')
    html = HTML("<h1>Hello World</h1>", encoding='utf-8')
    payload = [plaintext, html]

    headers = {
            "To": "janedoe@yahoo.com",
            "From": "johndoe@yahoo.com",
            "Subject": "Hello World",
            }

    envelope = mailthon.envelope.Envelope(headers, payload)


~~~~~~~~~~~~~~~~~~~~~~
Enclosure and Envelope
~~~~~~~~~~~~~~~~~~~~~~

It's worth noting that ``Envelope`` and ``Enclosure`` are conceptually similar: they are both made out of headers and content. In terms of mailthon's API, they function almost identically- they both provide the crucial mime() method that operates the heavy lifting of mailthon's ``Enclosure`` objects. 

However there are operational differences between the two. ``Enclosures`` have a ``content`` attribute that ``Envelope`` does not. Also, an ``Envelope`` can operate as an ``Enclosure`` but not vice versa; ``Enclosure`` lacks the concept of senders and receivers.

::

    ...
    >>> plaintext.headers
    {}
    >>> plaintext.mime()
    <email.mime.text.MIMEText object at 0x...>
    >>> plaintext.content
    "Hello World"
    >> envelope.headers
    {"To": "janedoe@yahoo.com", "From": "johndoe@yahoo.com", 
        "Subject": "Hello World"}
    >> envelope.mime()
    <email.mime.text.MIMEText object at 0x...>

The `mailthon docs <http://mailthon.readthedocs.org/en/latest/indepth.html#disecting-enclosures>`_ dissect the relationship between ``Enclosure`` and ``Envelope`` further.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Attachment and Binary Enclosure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Attachment`` can be used to turn a file on the system into an email and attachment. ``Attachment`` inherits from the ``Binary`` enclosure, which can be used to read files from the system, dynamically generated files, files from emails, etc. 

::

    import mailthon
    from mailthon.enclosure import PlainText, Attachment, Binary
    from mailthon.headers import content_disposition

    file_attachment = Attachment("text.txt")

    with open("sample.pdf", "rb") as attachment_file:  # rb for read binary
        binary_attachment_contents = attachment_file.read()

    binary_attachment = Binary(
            content=binary_attachment_contents,
            mimetype='application/pdf',
            headers=[content_disposition("attachment", "sample.pdf")],
            )

Take notice that ``Binary`` takes a bit more work than ``Attachment``. ``Attachment`` goes out of it's way to guess the files mimetype and add the Content-Disposition header which gives the attachment it's file name. These are both things we need to handle with the ``Binary`` enclosure.

~~~~~~~~~~~~~~~~~~~~~~~
User Defined Enclosures
~~~~~~~~~~~~~~~~~~~~~~~

We can define new classes that inherit from the base class ``Enclosure``. The only requirement that must be met is that the class method ``Enclosure.mime()`` returns a finalised mime object with all of it's mime headers.

This requirement can be satisfied by overriding the ``Enclosure.mime_object()`` method, which is called by ``Enclosure.mime()``. The ``Enclosure.mime()`` method prepares the object headers for you so you'd only have to worry about supplying the mime object.

::

    from mailthon.enclosure import Enclosure

    class NewEnclosure(Enclosure):
        
        def mime_object(self):
            return email.mime.text.MIMEText("Hello World")

    base_enclosure = Enclosure()
    base_enclosure.mime()  # will raise NotImplementedError

    new_enclosure = NewEnclosure()
    new_enclosure.mime()  # will return a headered MIME object now
