.. _imaplib_mailbox_wrapper:

this example can be found in **examples/imaplib_mailbox_wrapper/**

=============
IMAP4 Wrapper
=============

Although not a wrapper in the technical sense, this inherited class overrides
the methods of ``imaplib.IMAP4`` to make it even just *slightly* more pythonic.

This class has a lot of room for growth; there's a lot about ``imaplib`` that
is unpythonic. Whatever state this class is in, it's still better than using
the library raw. 

To download mailbox.py, :download:`click here<./mailbox.py>` (To actually download it, right click the link and select "Save link as...").


-----------------
The Mailbox Class
-----------------

The ``Mailbox`` class' goal is to remove the frustrating idosyncracies of using ``imaplib.IMAP4``, while preserving the same workflow.


^^^^^^^^^^^^^^^^
Current Features
^^^^^^^^^^^^^^^^

These features are currently implemented in ``mailbox.py``.

1. Filters out the ``status`` in methods that return a tuple of ``(status, data)``.
2. Raises ``Mailbox.MailboxException`` for any method that returns a non-OK ``status``.


^^^^^^^^^^^^^^^
Future Features
^^^^^^^^^^^^^^^

These are features that I can imagine being in ``mailbox.py`` in the future

1. Convert ``.fetch()`` results into a more readable result (parse RFC822 w/ ``email.parser``?).
2. ``with`` scope compatability for ``.select()`` and ``.close()`` folder
   selection (``IMAP4`` already supports this scope at instace level).
3. ``.append()`` can take an ``email.Email`` object
4. Overriding/overloading any ``mailbox`` arguments within the scope of
   ``.select()``


^^^^^^^^^^
mailbox.py
^^^^^^^^^^

Below is a full ``.. literalinclude::`` of the file **examples/imaplib_mailbox_wrapper/mailbox.rst**.


.. literalinclude:: mailbox.py
   :language: python


