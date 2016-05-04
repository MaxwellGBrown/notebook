<%inherit file="base.mako" />

<%def name="body()">

<div class="panel panel-default">
  <div class="panel-heading" data-toggle="collapse" data-target="#add-group-container">
    <div class="panel-title">Add New Group</div>
  </div>
  <%
if group_form.errors:
    container_class = "panel-body"
else:
    container_class = "panel-body collapse"
  %>
  <div id="add-group-container" class="${container_class}">
    <form class="form-horizontal" method="POST"
	action="${request.route_url('list_groups')}">
      ${form_group(group_form.groupname)}  
	  ${form_group(group_form.private)}
      <div class="form-group">
        <div class="col-sm-offset-2 col-sm-10">
          <button type="submit" class="btn btn-default">Submit</button>
        </div>
      </div>
    </form>
  </div>
</div>

<div class="list-group">
  % for group in groups:
	% if group is new_group:
      <a href="${request.route_url('group', group_id=group.id)}" class="list-group-item list-group-item-success">${group.groupname}</a>
	% else:
      <a href="${request.route_url('group', group_id=group.id)}" class="list-group-item">${group.groupname}</a>
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
