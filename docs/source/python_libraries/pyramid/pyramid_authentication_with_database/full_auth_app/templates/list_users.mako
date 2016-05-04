<%inherit file="base.mako" />

<%def name="body()">

<div class="panel panel-default">
  <div class="panel-heading" data-toggle="collapse" data-target="#add-user-container">
    <div class="panel-title">Add New User</div>
  </div>
  <%
if user_form.errors:
    container_class = "panel-body"
else:
    container_class = "panel-body collapse"
  %>
  <div id="add-user-container" class="${container_class}">
    <form class="form-horizontal" method="POST" action="${request.route_url('list_users')}">
      ${form_group(user_form.username)}  
      ${form_group(user_form.password)}
      ${form_group(user_form.match_password)}
      <div class="form-group">
        <div class="col-sm-offset-2 col-sm-10">
          <button type="submit" class="btn btn-default">Submit</button>
        </div>
      </div>
    </form>
  </div>
</div>

<div class="list-group">
  % for user in users:
    % if user is request.user:
      <a href="${request.route_url('user', user_id=user.id)}" class="list-group-item"><b>${user.username}</b></a>
	% elif user is new_user:
      <a href="${request.route_url('user', user_id=user.id)}" class="list-group-item list-group-item-success">${user.username}</a>
	% else:
      <a href="${request.route_url('user', user_id=user.id)}" class="list-group-item">${user.username}</a>
	% endif
  % endfor
</div>
</%def>

<%def name="form_group(field)">
<%
    if field.errors:
        div_class = "form-group has-error"
    else:
        div_class = "form-group"
%>
<div class="${div_class}">
  ${field.label(class_="col-sm-2 control-label")}
  <div class="col-sm-8">
    ${field(class_="form-control")}
	% for error in field.errors:
	  <span class="help-block">${error}</span>
	% endfor
  </div>
</div>
</%def>
