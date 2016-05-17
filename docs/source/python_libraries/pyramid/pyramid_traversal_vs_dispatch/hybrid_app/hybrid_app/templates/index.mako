<html>
<head>
    <title>Traversal App</title>
</head>
<body>
<div>
    <h1>Traversal App Index</h1>

	<h2>request.context: ${request.context.__repr__()}</h2>
	<p>
	  <b>Traversal</b> maps URLs to view callables by traversing the
	  <i>resource tree</i> based on the URL. The view is matched to a URL based
	  on...
	  </p>

	  <ol>
	    <li>
		  The final <i>resource</i> matched in the resource tree. This is the
		  <i>context</i> in the @view_config.
		</li>
	    <li>
		  The last piece of the URL not used to match a resource, which will
		  match a <i>view name</i>.
		</li>
	  </ol>

      <p>
	  By clicking the link below, you'll be traversing from the RootFactory to
	  the resource that matches "foo_tree", which is FooFactory. <br/>
	  <br/>
	  RootFactory(request)['foo_tree'] =&#62; FooFactory =&#62; Foo =&#62; Bar =&#62;
	  Baz =&#62; Qux <br/>
	  <br/>
	  <a href="${request.resource_url(request.context['foo_tree'], 'view')}">
	    Navigate foo_tree via Traversal
	  </a>
    </p>
</div>
</body>
</html>
