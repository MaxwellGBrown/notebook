<%inherit file="base.mako" />

<%def name="body()">
<form action="${request.route_url('login')}" method="POST">
  ${login_form.username.label} ${login_form.username()} <br/>
  % if login_form.username.errors:
    <ul>
    % for error in login_form.username.errors:
	  <li>${error}</li>
    % endfor
	</ul>
	<br/>
  % endif
  ${login_form.password.label} ${login_form.password()} <br/>
  % if login_form.username.errors:
    <ul>
    % for error in login_form.password.errors:
	  <li>${error}</li>
    % endfor
	</ul>
	<br/>
  % endif
  <input type="submit" value="Submit">
</form>
</%def>
