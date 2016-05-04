<%inherit file="base.mako" />

<%def name="body()">
<form action="${request.route_url('login')}" method="POST">
  ${login_form.username.label} ${login_form.username()} <br/>
  ${login_form.password.label} ${login_form.password()} <br/>
  <input type="submit" value="Submit">
</form>
</%def>
