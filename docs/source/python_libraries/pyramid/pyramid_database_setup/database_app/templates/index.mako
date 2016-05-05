<html>
<head>
  <title>database_app</title>
</head>
<body>
<h1>database_app</h1>
<h2>Add New Contact</h2>
  <form method="POST" action="${request.route_url('index')}">
    ${form.first_name.label()} ${form.first_name()}<br/>
    ${form.last_name.label()} ${form.last_name()}<br/>
    ${form.address.label()} ${form.address()}<br/>
	<input type="submit">
  </form>
<h2>All Contacts</h2>
  % for contact in contacts:
    <address>
      ${contact.first_name} ${contact.last_name} ${contact.address}
    </address>
  % endfor
</body>
</html>
