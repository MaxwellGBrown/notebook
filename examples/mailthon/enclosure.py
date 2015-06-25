"""
mailthon examples

==============
2-Enclosure.py
==============

An exploration of mailthon.enclosures and their relationship to the envelope
and mailthon.headers
"""


smtp = str(raw_input("SMTP server: "))
email = str(raw_input("Email address to test with: "))
password = str(raw_input("Password for {}: ".format(email)))
auth = (email, password)


import mailthon

# MIMEType text/plain
plaintext_contents = "This is the plain text enclosure!"
plaintext = mailthon.enclosure.PlainText(plaintext_contents, encoding='utf-8')

# MIMEType text/html
html_content = "<p>This is the <em>HTML</em> enclosure!</p>"
html = mailthon.enclosure.HTML(html_content, encoding='utf-8')

# file attachments. Attachment auto-populates the Content-Disposition header.
file_attachment = mailthon.enclosure.Attachment("./text.txt")

# binary attachments. Binary needs it's headers & MIMEtype populated
with open("sample.pdf", "rb") as attachment_file:  # rb for read binary
    binary_attachment_contents = attachment_file.read()

# mailthon.headers provides header formatting functions
from mailthon.headers import content_disposition
binary_attachment = mailthon.enclosure.Binary(
        content=binary_attachment_contents,
        mimetype='application/pdf',
        headers=[content_disposition('attachment', "sample.pdf")],
        )

# enclosures are added to a list to obstantiate Envelope
enclosures = [plaintext, html, file_attachment, binary_attachment]

headers = {
        "To": email,
        "From": email,
        "Subject": "2-Enclosure.py",
        }

envelope = mailthon.envelope.Envelope(headers, enclosures)

postman = mailthon.postman(smtp, auth=auth)
postman.send(envelope)
