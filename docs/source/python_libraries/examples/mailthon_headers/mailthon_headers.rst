================
Mailthon Headers
================

--------------
Headers Basics
--------------
``Headers`` are used to simplify the crafting of headers in MIME objects. mailthon ``Headers`` are used in both ``Envelope`` and ``Enclosure``, although ``Headers`` have more responsibility in the former in that they must handle who is sending to whom. 

``Headers`` is a child of a ``UnicodeDict``, forcing all of it's value entries into Unicode. ``Headers`` also handles the creation of rfc 2822 compliant email headers so we do not have to worry about formatting them.

``Headers`` can be initialized as an object, or inside the init arguments for ``Enclosures`` and ``Envelope``. ``Headers`` first positional argument, or the keyword ``values`` is an iterable of values (e.g. a ``dict``, a ``list`` of pairs, a ``generator`` of pairs, etc.)

::

    from mailthon.headers import Headers
    from mailthon.envelope import Envelope

    unformatted_headers = {
        "To": "janedoe@gmail.com",
        "From": "johndoe@gmail.com",
        "Subject": "Hello World",
    }
    headers = Headers(values=unformatted_headers, encoding='utf-8')

    envelope = Envelope(headers, [])


--------------------------
mailthon.headers functions
--------------------------
``mailthon.headers`` also provides functions that make it easier to programmatically write headers. ``Binary``, unlike ``Attachment`` doesn't give the appropriate attachment header to the file. But we can take advantage of ``mailthon.headers.content_disposition()`` just like ``Attachment`` does to give it one!

::

    import mailthon.headers
    from mailthon.headers import Headers

    from mailthon.enclosure import Binary
    from mailthon.envelope import Envelope

    unformatted_headers = [
        mailthon.headers.subject("Hello World"),
        mailthon.headers.sender("jondoe@gmail.com"),
        mailthon.headers.to("janedoe@gmail.com", "jessiedoe@gmail.com"),
        mailthon.headers.cc("jonsmith@yahoo.com", "janesmith@gmail.com"),
        mailthon.headers.bcc("juancabrera@yahoo.com", "hanwan@gmail.com"),
        mailthon.headers.date(),  # automatically puts in current time
    ]
    headers = Headers(unformatted_headers)

    with open("sample.pdf", "rb") as pdf_attachment_file:
        pdf_attachment_binary = pdf_attachment_file.read()
    attachment_headers = [
            mailthon.headers.content_disposition("attachment", "sample.pdf"),
    ]
    pdf_attachment = Binary(
            content=pdf_attachment_binary,
            mimetype="application/pdf",
            headers=attachment_headers,
    )

    envelope = Envelope(headers, [pdf_attachment])
