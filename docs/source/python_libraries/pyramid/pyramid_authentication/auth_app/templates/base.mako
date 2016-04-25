<HTML>

<head>
  <title>${self.title()}</title>
  ${self.head()}
</head>

<body>
  ${self.navigation()} 
  <h1>${self.title()}</h1>
  <div class="container">
  % if request.user:
    <p class="lead">Logged in as ${request.user.username}</p>
  % endif
    ${next.body()}
  </div>
</body>

</HTML>

<%def name="title()">
Pyramid Auth
</%def>

<%def name="navigation()">
<ul id="navigation" class="nav nav-tabs nav-justified">
  <li><a href="${request.route_url('index')}">Index</a></li>
  <li><a href="${request.route_url('admin')}">Admin</a></li>
  <li><a href="${request.route_url('public')}">Public</a></li>
  <li><a href="${request.route_url('login')}">Login</a></li>
  <li><a href="${request.route_url('logout')}">Logout</a></li>
</ul>
</%def>

<%def name="head()">
<!-- jQuery required for Bootstrap -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

<!-- Bootstrap Javascript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>

<!-- Bootstrap Styling -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
</%def>
