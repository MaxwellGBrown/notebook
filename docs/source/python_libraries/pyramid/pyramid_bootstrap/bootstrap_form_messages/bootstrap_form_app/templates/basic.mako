<html>

<head>
    <title>Bootstrap Form Messages</title>

    <!-- jQuery required for Bootstrap -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    
    <!-- Bootstrap Javascript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
    
    <!-- Bootstrap Styling -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

</head>

<body>
  
<div class="container">

  <h1>Bootstrap Form Messages</h1>
  
  <br/>

  <p class="lead">
    With some basic mako templating and wtform's validation messages, some
	really good error messages can be paired with their inputs and bootstrap
	styling.
  </p>

  <p class="text-center">${message}</p>

  <form class="form-horizontal" action="${request.route_url('index')}" method="POST">
    ${make_form_group(form, "username")}
    ${make_form_group(form, "email")}
    ${make_form_group(form, "password")}
    <div class="form-group">
      <div class="col-sm-offset-2 col-sm-10">
        <button type="submit" class="btn btn-default">Submit</button>
      </div>
    </div>
  </form>

</div>

</body>

</html>

<%def name="make_form_group(form, fieldname)">
<%
    field = getattr(form, fieldname)
    if field.errors:
        div_class = "form-group has-error"
    else:
        div_class = "form-group"
%>
  <div class="${div_class}">
    ${field.label(class_="col-sm-2 control-label")}
	<div class="col-sm-8">
	  ${field(class_='form-control')}
	  % for error in field.errors:
	    <span class="help-block">${error}</span>
	  % endfor
	</div>
  </div>
</%def>
