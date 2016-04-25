from pyramid.security import unauthenticated_userid

class User(object):

    def __init__(self, userid, username, password, user_type="user"):
        self.userid = userid
        self.username = username
        self.password = password
        if user_type == "admin":
            self.user_type = "admin"
            self.groups = ["group:admin"]
        else:
            self.user_type = "user"
            self.groups = ['group:user']


USERS = {
        User(1, "admin_user", "hunter2", "admin"),
        User(2, "normal_user", "password1", "user"),
        }


def get_user(request):
    """
    request.user - config.add_request_method(get_user, 'user', reify=True)
    """
    userid = unauthenticated_userid(request)
    if userid is not None:
        for user in USERS:
            if user.userid == userid:
                return user
        else:
            return None


def groupfinder(userid, request):
    """
    AuthTktAuthenticationPolicy(..., callback=groupfinder, ...)

    relies on request.user from ``get_user(request)``
    """
    user = request.user
    if user is not None:
        return user.groups
    else:
        return None
