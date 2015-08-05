import email
import mailthon


def message_into_envelope(message):
    """
    Returns a mailthon.envelope.Envelope of the email.message

    Copies all headers from the original message.
    Turns all mime-parts into enclosures.
    """
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
