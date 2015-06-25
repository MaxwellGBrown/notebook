"""
mailthon examples

===========
1-Basics.py
===========

This outlines the basics of setting up an SMTP connection and sending mail

"""

import mailthon


smtp = str(raw_input("email server: "))
email = str(raw_input("email address: "))
password = str(raw_input("password for {}: ".format(email)))

# make a connection to the SMTP server
auth = (email, password)
postman = mailthon.postman(host=smtp, auth=auth)

# set up the email headers
headers = {
        "To": "mbrown@morpace.com",
        "From": "mbrown@morpace.com",
        "Subject": "1-Basics.py",
        }

# create the contents of the email with mailthon.enclosures
plaintext = mailthon.enclosure.PlainText("Hello World")
enclosures = [plaintext]

# obstantiate the email envelope with the headers dict and enclosures list
envelope = mailthon.envelope.Envelope(headers, enclosures)

# send the envelope with the postman/SMTP connection
response = postman.send(envelope)
print "response.ok: " + str(response.ok)
print "response.status_code: " + str(response.status_code)
print "response.message: " + str(response.message)
print "response.rejected: " + str(response.rejected)
