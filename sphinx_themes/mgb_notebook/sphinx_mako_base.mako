<html>
	<head>
	  ${self.css()}
	</head>

	<body>
		${next.body()}
	</body>
</html>

<%def name="css()">
    <link rel="stylesheet" href="${'_static/' + sphinx_context['style']}" type="text/css" />
    <link rel="stylesheet" href="_static/pygments.css" type="text/css" />
	% for css_file in sphinx_context['css_files']:
    <link rel="stylesheet" href="${css_file}" type="text/css" />
	% endfor
</%def>
