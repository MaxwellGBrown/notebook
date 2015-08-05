"""
mailthon examples

============
3-Headers.py
============

An example of using the suggested header functions provided with mailthon.
"""


smtp = str(raw_input("mail server: "))
email = str(raw_input("email address: "))
password = str(raw_input("password for {}: ".format(email)))
auth = (email, password)


import mailthon

# we can appropriately craft the Headers for the mailthon envelope using
# mailthon.headers

# the headers for Envelope can be any iterable that returns key-value pairs.
# a a dictionary, a list of 2 item generators (the headers fxns are these),
# a list of tuples, etc.
headers = [
        mailthon.headers.to(email),  # uses *args
        mailthon.headers.cc(email),  # uses *args
        mailthon.headers.bcc(email),  # uses *args
        mailthon.headers.sender(email),
        mailthon.headers.subject("3-Headers.py"),
        mailthon.headers.date(),
        mailthon.headers.message_id(),
        ]
# mailthon comes with a Headers class that magically encodes everything in
# Unicode that we can use. It operates like dict (and inherits from dict too)
headers_obj = mailthon.headers.Headers(headers)
# rfc 2822 says that Sender should be sufficient if From doesn't exist, but
# I've noticed that this is often not the case
headers_obj['From'] = email

# note that if you're opening a file to read it as a binary, you'd probably be
# better off using the Attachment enclosure. This is just an example though.
with open("sample.pdf", "rb") as pdf_attachment_file:
    pdf_attachment_binary = pdf_attachment_file.read()

# as mentioned in 2-Enclosure.py, Binary enclosures need to have their headers
# manually filled. These can be done using mailthon.headers.content_disposition
pdf_attachment = mailthon.enclosure.Binary(
        content=pdf_attachment_binary,
        mimetype="application/pdf",
        headers=[
            mailthon.headers.content_disposition("attachment", "sample.pdf"),
            ],
        )

enclosures = [mailthon.enclosure.PlainText("3-Headers.py"), pdf_attachment]

postman = mailthon.postman(smtp, auth=auth)
postman.send(mailthon.envelope.Envelope(headers_obj, enclosures))
