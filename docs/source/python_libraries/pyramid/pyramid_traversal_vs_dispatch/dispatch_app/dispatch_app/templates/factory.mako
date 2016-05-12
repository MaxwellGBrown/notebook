<html>
<head>
    <title>${title}</title>
</head>
<body>
<div>
    <h1>${title}</h1>

    % if baz is not None:
	  <h2>/factory/{foo}/{bar}/{baz}</h2>
	  <h2>/factory/${foo}/${bar}/${baz}</h2>
	% elif bar is not None:
	  <h2>/factory/{foo}/{bar}</h2>
	  <h2>/factory/${foo}/${bar}</h2>
	% elif foo is not None:
	  <h2>/factory/{foo}</h2>
	  <h2>/factory/${foo}</h2>
	% endif


	% if foo is not None:
	  <p>
	    foo: ${foo} <br/>
		<a href="${request.route_url('factory_foo', foo=foo)}">
		  ${request.route_path('factory_foo', foo=foo)}
		</a>
	  </p>
	% endif

	% if bar is not None:
	  <p>
	    bar: ${bar}<br/>
		<a href="${request.route_url('factory_bar', foo=foo, bar=bar)}">
		  ${request.route_path('factory_bar', foo=foo, bar=bar)}
		</a>
	  </p>
	% endif

	% if baz is not None:
	  <p>
	    baz: ${baz}<br/>
		<a href="${request.route_url('factory_baz', foo=foo, bar=bar, baz=baz)}">
		  ${request.route_path('factory_baz', foo=foo, bar=bar, baz=baz)}
		</a>
	  </p>
	% endif
</div>
</body>
</html>
