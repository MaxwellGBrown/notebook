import imaplib


class Mailbox(imaplib.IMAP4):
    """
    imaplib.IMAP4 wrapper that filters out status from data
    """

    def __init__(self, host, *args, **kwargs):
        super().__init__(host, *args, **kwargs)

    class MailboxException(BaseException):
        """A custom exception for NO or BAD"""
        def __init__(self, status, data):
            response = b" ".join(data).decode("UTF-8")
            self.message = "{}: {}".format(status, response)

        def __str__(self):
            return self.message

    def login(self, username, password):
        try:
            super().login(username, password)
        except imaplib.IMAP4.error:  # bad authentication
            raise self.MailboxException(b"BAD", [b"Authentication Failed"])

    def list(self, *args, **kwargs):
        status, data = super().list(*args, **kwargs)
        if status != "OK":
            raise self.MailboxException(status, data)
        else:
            return data

    def create(self, mailbox, *args, **kwargs):
        status, data = super().create(mailbox, *args, **kwargs)
        if status != "OK":
            raise self.MailboxException(status, data)
        else:
            return data

    def select(self, mailbox="INBOX", *args, **kwargs):
        status, data = super().select(mailbox, *args, **kwargs)
        if status == "OK":
            return int(data[0])  # number of messages in mailbox
        else:
            raise self.MailboxException(status, data)

    def fetch(self, *args, **kwargs):
        status, data = super().fetch(*args, **kwargs)
        if status != "OK":
            raise self.MailboxException(status, data)
        else:
            return data

    def expunge(self):
        status, data = super().expunge()
        if status != "OK":
            raise self.MailboxException(status, data)
        else:
            return data

    def status(self, *args, **kwargs):
        # try:
        status, data = super().status(*args, **kwargs)
        # except imaplib.IMAP4.error as error:
        #     raise Exception("Could not get server status!")
        if status != "OK":
            raise self.MailboxException(status, data)
        else:
            return data

    def close(self):
        status, data = super().close()
        if status != "OK":
            raise self.MailboxException(status, data)
        else:
            return data

    def uid(self, *args, **kwargs):
        """
        Work with emails using their UID as an identifier.

        The issue with the UID function is that, unless there's an error with
        the actual arguments you supply the IMAP4.uid function, the response
        will **ALWAYS** be OK.

        For the most part, the server has responses if you try to access a UID
        that doesn't exist, or perform an action that does not succeed

        e.g. IMAP4.uid('FETCH', 999999, '(RFC822)') -> NO ['Email gone']

        Frustratingly, there are situations where the action may succeed/fail
        with no difference in output.

        e.g. IMAP4.uid('COPY') --ALWAYS--> (OK, [None]), even if failure
        """
        # try:
        status, data = super().uid(*args, **kwargs)
        # except imaplib.IMAP4.error as error:
        #     raise Exception(error)
        if status != "OK":
            raise self.MailboxException(status, data)
        return data

