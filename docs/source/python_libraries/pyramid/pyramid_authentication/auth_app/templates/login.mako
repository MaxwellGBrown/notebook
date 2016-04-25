<%inherit file="base.mako" />

<%def name="body()">
<form action="${request.route_url('login')}" method="POST">
  ${login_form.login.label} ${login_form.login()} <br/>
  ${login_form.password.label} ${login_form.password()} <br/>
  <input type="submit" value="Submit">
</form>
</%def>
