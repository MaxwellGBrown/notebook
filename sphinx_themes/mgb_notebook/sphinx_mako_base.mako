<html>
	<head>
	  <title>${title}</title>
	  ${self.css()}
	  ${self.js()}

	  % if use_opensearch:
          <link rel="search" type="application/opensearchdescription+xml"
                title="Search within ${docstitle}"
                href="${pathto('_static/opensearch.xml', 1)}"/>
	  % endif

	  % if favicon:
	    <link rel="shortcut icon" href="${pathto('_static/' + favicon, 1)}" />
	  % endif

	  ${self.linktags()}

	</head>

	<body role="document">
	    ## relbar1
	    ${self.relbar()}
		
		${next.body()}
		
	    ## relbar2
		${self.relbar()}
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

<%def name="linktags()">

	## about page
	% if hasdoc('about'):
    <link rel="author" title="${'About these documents'}" href="${pathto('about')}" />
	% endif

	## master index page
    % if hasdoc('genindex'):
    <link rel="index" title="${'Index'}" href="${pathto('genindex')}" />
    % endif

	## search page
    % if hasdoc('search'):
    <link rel="search" title="${'Search'}" href="${pathto('search')}" />
    % endif

	## copyright page
    % if hasdoc('copyright'):
    <link rel="copyright" title="${'Copyright'}" href="${pathto('copyright')}" />
    % endif

	## top of page
    <link rel="top" title="${docstitle}" href="${pathto(master_doc)}" />

	## next parent page
    % if parents:
    ## <link rel="up" title="${parents[-1].title}" href="${parents[-1]link}" />
    <link rel="up" title="${parents[-1].get('title')}" href="${parents[-1].get('link')}" />
    % endif

	## next page in order
    % if sphinx_next:
    ## <link rel="next" title="${sphinx_next.title}" href="${sphinx_next.link}" />
    <link rel="next" title="${sphinx_next.get('title')}" href="${sphinx_next.get('link')}" />
    % endif

	## previous page in order
    % if prev:
    ## <link rel="prev" title="${prev.title}" href="${prev.link}" />
    <link rel="prev" title="${prev.get('title')}" href="${prev.get('link')}" />
    % endif

</%def>

<%def name="relbar()">
    <div class="related" role="navigation">
	  <h3>Navigation</h3>
	  <ul>
	    % for rellink in rellinks:
		  <li class="right">
		  ##   <a href="${pathto(rellink[0])}" title="${rellink[1]}" ${accesskey(rellink[2])}>${rellink[3]}</a>
		    <a href="${pathto(rellink[0])}" title="${rellink[1]}">${rellink[3]}</a>
		  </li>
		% endfor

	    <li class="nav-item nav-item-0"><a href="${pathto(master_doc)}">${shorttitle}</a></li>

		% for sphinx_parent in parents:
		  <li class="nav-item nav-item-${parents.index(sphinx_parent)}"><a href="${sphinx_parent.get('link')}">${sphinx_parent.get('title')}</a>
		  ## <li class="nav-item nav-item-${parents.index(sphinx_parent)}"><a href="${parent.link}">${parent.title}</a>
		% endfor
	  </ul>

	</div>
</%def>
