<%inherit file="base.mako" />

<%def name="body()">
<h2>${group.groupname}</h2>
% if group.private is True:
  <p>This group is private, non-members will get 403'd on this page!</p>
% else:
  <p>This group is public, Auth'd users will get 200'd while requesting this
  page!</p>
% endif

<p>
  % if request.user in group.get_members():
    <a href="${request.route_url('leave_group', group_id=group.id)}">
      Leave this group
    </a>
  % else:
    <a href="${request.route_url('join_group', group_id=group.id)}">
	  Join this group
	</a>
  % endif
</p>


<h3>Members</h3>
  <ul>
    % for user in members:
	  <li>
	    <a href="${request.route_url('user', user_id=user.id)}">
		% if user is request.user:
		  <b>
		% endif
	      ${user.username}
	    % if user is request.user:
          </b>
        % endif
        </a>
        % if group.is_admin(user) is True:
          (admin)
        % endif
	  </li>
	% endfor
  </ul>
</%def>
