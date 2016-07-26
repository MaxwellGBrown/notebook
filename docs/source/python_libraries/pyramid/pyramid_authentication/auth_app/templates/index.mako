<%inherit file="base.mako" />

<%def name="body()">
<h2>This is the Index!</h2>

% if request.user is None:
  <form method="POST" action="${request.route_url('index')}">
    <h2>Register</h2>
	${user_form.username(placeholder="Username")}<br/>
	% for error in user_form.username.errors:
	  <span>${error}</span>
	% endfor
	${user_form.password(placeholder="Password")}<br/>
	<input type="submit"/>
  </form>
% else:
  Log out if you'd like to register another user.
% endif
</%def>
