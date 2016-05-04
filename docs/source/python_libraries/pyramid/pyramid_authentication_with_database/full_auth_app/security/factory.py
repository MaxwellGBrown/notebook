from pyramid.security import Allow, Everyone, Authenticated

from full_auth_app.model.auth import get_users, get_groups


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
            # (Allow, Authenticated, "view"),
            (Allow, "group:admin", "admin"),
            ]

    def __init__(self, request):
        self.request = request


class UserFactory(object):
    __acl__ = [
            (Allow, Authenticated, "view"),
            ]

    def __init__(self, request):
        self.request = request

    def __getitem__(self, user_id):
        users = get_users(id=user_id)
        if users:
            return users[0]
        else:
            return None


class GroupFactory(object):
    __acl__ = [
            (Allow, Authenticated, "view"),
            ]

    def __init__(self, request):
        self.request = request

    def __getitem__(self, group_id):
        groups = get_groups(id=group_id)
        if groups:
            return groups[0]
        else:
            return None
