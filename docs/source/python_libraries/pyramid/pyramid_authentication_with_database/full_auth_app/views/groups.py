from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from full_auth_app.model.auth import all_groups, new_group, get_groups


@view_config(route_name="list_groups",
        renderer="full_auth_app:templates/list_groups.mako")
def list_groups(request):
    form = GroupForm(request.POST)
    if request.method == "POST" and form.validate():
        added_group = new_group(groupname=form.groupname.data,
                private=form.private.data)
        added_group.add_member(request.user, is_admin=True)
    else:
        added_group = None
    return {
            "groups": all_groups(),
            "new_group": added_group,
            "group_form": form
            }

@view_config(route_name="group", renderer="full_auth_app:templates/group.mako",
        permission="view")
def group_view(request):
    """ request.context is a Group gathered by GroupFactory """
    members = request.context.get_members()
    return {"group": request.context, "members": members}

@view_config(route_name="join_group")
def join_group(request):
    request.context.add_member(request.user)
    raise HTTPFound(request.route_url("group", group_id=request.context.id))

@view_config(route_name="leave_group")
def leave_group(request):
    request.context.remove_member(request.user)
    raise HTTPFound(request.route_url("group", group_id=request.context.id))


from wtforms import Form, StringField, BooleanField, validators as val
from wtforms.validators import ValidationError


def unique_groupname(form, field):
    all_groupnames = [g.groupname for g in all_groups()]
    if field.data in all_groupnames:
        raise ValidationError(field.data + " is already being used!")


class GroupForm(Form):
    groupname = StringField("Group Name",
            validators=[unique_groupname, val.Length(min=6)])
    private = BooleanField("Only members can see group page", default=False)
