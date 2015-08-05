==============================
mailthon and the email library
==============================

This section highlights some examples of working with ``mailthon`` and ``email``.

======================================
Turning email.Message into an envelope
======================================

``mailthon`` takes a lot of advantage of ``email`` MIME objects. However, we need to manage how to take the different character sets of text parts and different encoding of non-text parts and structure them into ``Enclosure`` objects and convert the email's headers into ``Headers`` objects. 

On top of this, just as ``Envelopes`` can also operate as ``Enclosure`` objects, we can have emails imbedded into emails as multipart sections, and/or multiple email parts embedded as multipart sections.


.. literalinclude:: email_to_mailthon.py
    :language: python
    :caption: email_to_mailthon.py


To grab all of the parts of the message if it is a multipart message, we use the recursive function ``message_into_enclosures``. It breaks down each message part until it is no longer multipart and then returns an enclosure for it.

``message_into_envelope`` leverages ``message_into_enclosures`` to get enclosures for the message parts, but uses the message headers from the highest level for the envelope.
