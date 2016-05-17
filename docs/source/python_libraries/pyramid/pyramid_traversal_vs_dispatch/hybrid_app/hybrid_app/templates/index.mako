<html>
<head>
    <title>Hybrid Traversal App</title>
</head>
<body>
<div>
    <h1>Hybrid Traversal App Index</h1>
	<p>
	  Hybrid Traversal is essentially a Traversal application that leverages
	  routes to match requests to different RootFactories to operate the
	  traversal of their resource trees. <br/>
	  <br/>
	  In this example, FooFactory is a separate root_factory that's supplied
	  specifically for routes that need to traverse, instead of as the
	  applications root_factory. <br/>
	  <br/>
	  <a href="${request.resource_url(view_root_factory, route_name='view')}">View route_name="view" w/ Hybrid
	  Traversal!</a>
	</p>
</div>
</body>
</html>
