=======
imaplib
=======

``imaplib`` is a package that communicates with an IMAP server, which is used to store email.

IMAP is specified by `RFC3501 <https://tools.ietf.org/html/rfc3501>`_ and, although ``imaplib`` hanldes a *bit* of the communication, a lot of the functions/methods require an understanding of RFC3501 & it's commands.

----------
Quickstart
----------

There's a basic scope in which the ``IMAP4`` object lives in...

::

  # Obstantiate object w/ web server  # IMAP4()
  #     Authenticate as a user        # IMAP4.login()
  #         Select a mailbox          # IMAP4.select()
  #             Perform operation     # e.g. IMAP4.fetch()
  #         Close mailbox             # IMAP4.close()
  #     Logout                        # IMAP4.logout()

After an ``IMAP4`` object enters UNAUTH mode then the object is locked, and no more operations can be done.

The only scope that can be explicitly forced is the instance scope of ``IMAP4``:

.. code-block:: python

  from imaplib import IMAP4

  with IMAP4("gmail.com") as mail:        # connect to mail server
      mail.login("jsmith", "hunter2")        # authenticate
      mail.select("INBOX")                   # open INBOX
      mail.store("*", "+FLAGS", "(\\Seen)")  # operation
      mail.close()                           # close INBOX
      # mail.logout()  # automatically called after __with__ scope ends


.. note::

  Any *message_set* args to IMAP4's methods are a string specifying what messages to be acted on.

  * '1' - Operate on message 1
  * '2:4' - Operate on messages 2-4
  * '1,3' - Operate on messages 1 & 3
  * '\*' - Operate on the most recent message
  * '1:\*' - Operate on all messages
  * '3:\*' - Operate on all messages after and including 3
  * '1,4,6:\*' - Operate on messages 1, 4, and everything after and including 6


imaplib doesn't filter the 3 basic server responses (``OK``, ``NO``, and ``BAD``).

This (annoyingly) means that most method calls will return a tuple of ``status, data``.

Since ``BAD`` & ``NO`` mean that the intended operation failed, the ``status`` portion needs to be checked *every time a command is run* to ensure that a chain of command dies on a failure (extremely frustrating).


.. code-block:: python

  with IMAP4("gmail.com") as mail:
      mail.login("jsmith", "hunter2")
      status, data = mail.select("Inbox/Foo")
      if status != "OK":
          raise Exception("Couldn't select \"Inbox/Foo\"")


--------------------------------
Basic IMAP Operations w/ imaplib
--------------------------------

This section outlines how one might use an already obstantiated IMAP4 object to do some basic IMAP operations.

.. code-block:: python

  from imaplib import IMAP4

  mail = IMAP4("gmail.com")
  mail.login("jsmith", "hunter2")


^^^^^^^^^^^^^^^^^^
Get Email Contents
^^^^^^^^^^^^^^^^^^

To get the email contents, IMAP4 can retrieve the RFC822 of an email, which is it's complete content.

The RFC822 can be parsed by ``email.parser.Parser()`` to be read programmatically.

.. code-block:: python

  status, data = mail.select("Inbox")
  status, data = mail.fetch("1:*", "(RFC822)")

  rfc822_dict = dict()
  for email_data in data:
      # [(b"1 (RFC822 {<size>}", b"<rfc822>"), ")", ...]
      if isinstance(email_data, tuple):
          imap_info = email_data[0].decode("UTF-8")
          key = imap_info[:imap_info.find(" (RFC822")]
          rfc822 = email_data[1].decode("UTF-8")

          rfc822_dict[key] = rfc822


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Move Emails To A Different Mailbox
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There's no MOVE IMAP command. Because of this, a move needs to be done with a combination of COPY & storing ``\Deleted`` flags.

.. code-block:: python

  status, data = mail.select("Inbox/Foo")

  status, data = mail.copy("2:4", "Inbox/Bar")
  if status != "OK":
      raise Exception("Could not copy messages 2:4 from Inbox/Foo to Inbox/Bar")

  status, data = mail.store("2:4", "+FLAGS", "(\\Deleted)")
  if status != "OK":
      raise Exception("Could not store \\Deleted for messages 2:4 in Inbox/Foo")

  status, data = mail.expunge()
  if status != "OK":
      raise Exception("Could not expunge Inbox/Bar after adding \\Deleted flags")


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Import RFC822 From File Into IMAP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes it's necessary to load a ``.eml`` file (which is just RFC822) into the mailbox.

.. code-block:: python

  folder = "Inbox/Foo"
  flags = ""
  date = "Tue, 8 Mar 2016 12:59:36 -0500"

  with open("~/Documents/email_file.eml", 'r') as email_file:
      status, data = self.mailbox.append(folder, flags, date, email_file.read())

  if status != "OK":
      raise Exception("Could not write email_file.eml to Inbox/Foo")
