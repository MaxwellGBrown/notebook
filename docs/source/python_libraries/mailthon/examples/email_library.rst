==============================
mailthon and the email library
==============================

This section highlights some examples of working with ``mailthon`` and ``email``.

======================================
Turning email.Message into an envelope
======================================

``mailthon`` takes a lot of advantage of ``email`` MIME objects. However, we need to manage how to take the different character sets of text parts and different encoding of non-text parts and structure them into ``Enclosure`` objects and convert the email's headers into ``Headers`` objects. 

On top of this, just as ``Envelopes`` can also operate as ``Enclosure`` objects, we can have emails imbedded into emails as multipart sections, and/or multiple email parts embedded as multipart sections.

::

    import email
    import mailthon

    def message_into_envelope(message):
        headers = mailthon.headers.Headers(message.items())
        enclosures = message_into_enclosures(message)
        return mailthon.envelope.Envelope(headers, enclosures)

    def message_into_enclosures(message):
        """
        Recursively turns multipart emails into an enclosure list
        """
        # basis
        if message.is_multipart() is False:
            content_type = message.get_content_type()
            payload = message.get_payload(decode=True)  # converts base64 for us
            charset = message.get_content_charset()
            if content_type == "text/html":
                enc = mailthon.enclosure.HTML(payload, encoding=charset)
            elif content_type == "text/plain":
                enc = mailthon.enclosure.PlainText(payload, encoding=charset)
            else:
                enc = mailthon.enclosure.Binary(
                        content=payload,
                        mimetype=content_type,
                        headers=message.items(),
                        )
            return [enc]
    
        # induction
        else:
            enclosures = list()
            for message_part in message.get_payload():
                new_enclosures = message_into_enclosures(message_part)
                enclosures.extend(new_enclosures)
            return enclosures

To grab all of the parts of the message if it is a multipart message, we use the recursive function ``message_into_enclosures``. It breaks down each message part until it is no longer multipart and then returns an enclosure for it.

``message_into_envelope`` leverages ``message_into_enclosures`` to get enclosures for the message parts, but uses the message headers from the highest level for the envelope.
