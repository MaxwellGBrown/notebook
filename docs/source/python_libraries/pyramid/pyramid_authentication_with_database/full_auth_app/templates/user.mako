<%inherit file="base.mako" />

<%def name="body()">
<h2>${user.username}</h2>
<h3>${user.username}'s Groups</h3>
<ul>
  % for group in user.get_groups():
    <li>
	  <a href="${request.route_url('group', group_id=group.id)}">
	    ${group.groupname}
	  </a>
	</li>
  % endfor
</ul>
</%def>
