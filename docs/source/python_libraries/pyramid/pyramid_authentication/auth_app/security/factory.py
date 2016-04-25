from pyramid.security import Allow, Everyone, Authenticated


class RootFactory(object):
    """
    This is how the application applies permissions to groups/users.

    It's applied in app_config via config.set_root_factory(RootFactory)

    ACL: "Access Control List", a sequence of ACE touples.
         e.g. __acl__ = [...]
    ACE: "Access Control Entry", one element in the ACL.
         e.g. (Allow, 'bob', 'read')
         Composed of 3 things:
             1. An Action (Allow or Deny) (e.g. Allow)
             2. A Principal (a string describing a user or group) (e.g. 'bob')
             3. A Permission (e.g. 'read')
    """
    __acl__ = [
            (Allow, Authenticated, "view"),
            (Allow, "group:admin", "admin"),
            ]

    def __init__(self, request):
        self.request = request
