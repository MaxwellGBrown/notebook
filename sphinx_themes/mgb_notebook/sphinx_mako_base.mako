<html>
	<head>
	  <title>${title}</title>
	  ${self.css()}
	  ${self.js()}
	  % if use_opensearch:
	    ${self.opensearch()}
	  % endif
	  % if favicon:
	    <link rel="shortcut icon" href="${pathto('_static/' + favicon, 1)}" />
	  % endif

	</head>

	<body>
		${next.body()}
	</body>
</html>

<%def name="css()">
    <link rel="stylesheet" href="${pathto('_static/' + style, 1)}" type="text/css" />
    <link rel="stylesheet" href="${pathto('_static/pygments.css', 1)}" type="text/css" />
	% for css_file in css_files:
    <link rel="stylesheet" href="${pathto(css_file, 1)}" type="text/css" />
	% endfor
</%def>

<%def name="js()">
    <script type="text/javascript">
      var DOCUMENTATION_OPTIONS = {
        URL_ROOT:    '${"" if pathto("", 1) == "#" else pathto("", 1)}',
        VERSION:     '${release}',
        COLLAPSE_INDEX: false,
        FILE_SUFFIX: '${'' if no_search_suffix else file_suffix}',
        HAS_SOURCE:  ${"true" if has_source else "false"}
      };
    </script>
	% for script_file in script_files:
    <script type="text/javascript" src="${pathto(script_file, 1)}"></script>
	% endfor
</%def>

<%def name="opensearch()">
    <link rel="search" type="application/opensearchdescription+xml"
          title="Search within ${docstitle}"
          href="${pathto('_static/opensearch.xml', 1)}"/>
</%def>
