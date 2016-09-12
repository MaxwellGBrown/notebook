<html>
	<head>
	  <title>${title or docstitle}</title>

	  ${self.js()}
	  ${self.css()}

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
        ${self.header()}

	    ## relbar1
	    ${self.relbar("fixed-top")}

		## Page structure based off of 
		## https://github.com/BlackrockDigital/startbootstrap-simple-sidebar
		<div id="main-wrapper">
		  ## render available sidebars?
		  <% include_sidebars = not embedded and not theme_nosidebar and sidebars != [] %>
		  % if include_sidebars is True:
		    <div id="sidebar-wrapper" class="col-sm-3">
		      ${self.render_sidebar()}
		    </div>

		    <div id="sidebar-toggle">
		      
		    </div>
		  % endif

		  
		  <div id="page-content-wrapper" class="col-sm-9">
		    <div class="container-fluid">
		      <div class="row">
		  	    <div id="content-container">

                  ${next.body()}

		  	      % if context.get("theme_include_debug") is not UNDEFINED:
		              ${debug()}
		  	      % endif
		  	    </div>
		  	  </div>
		    </div>
		  </div>

		</div> <!-- main-wrapper -->
		
	    ## relbar2
		${self.relbar("fixed-bottom")}

		${self.footer()}

		<script>
		  $("#sidebar-toggle").click(function(e) {
		 	e.preventDefault(); 
			$("#sidebar-wrapper").toggleClass("toggled");
			$("#sidebar-wrapper").toggleClass("col-sm-3");

			$("#page-content-wrapper").toggleClass("col-sm-9");
			$("#page-content-wrapper").toggleClass("col-sm-12");
		  });
		</script>

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

<%def name="header()">
  <header>
    Header
  </header>
</%def>

<%def name="relbar(*nav_classes)">
    <% nav_class = " ".join(["navbar"] + list(nav_classes)) %>
    <nav class="related ${nav_class}" role="navigation">
	  <div class="container">
	    <div class="navbar-header">
	      <a class="navbar-brand" href="${pathto(master_doc)}">${shorttitle}</a>
	      <ul class="nav navbar-nav pull-xs-right">

			% if context.get("theme_include_debug") is not UNDEFINED:
			  <li class="nav-item">
                <a href="#" class="nav-link" data-toggle="modal" data-target="#debug_modal">debug</a>
			  </li>
			% endif

	        % for rellink in rellinks:
	          <li class="nav-item">
	            <a class="nav-link" href="${pathto(rellink[0])}" title="${rellink[1]}">${rellink[3]}</a>
	            ##   <a href="${pathto(rellink[0])}" title="${rellink[1]}" ${accesskey(rellink[2])}>${rellink[3]}</a>
	          </li>
	        % endfor

	        % for sphinx_parent in parents:
	          <li class="nav-item nav-item-${parents.index(sphinx_parent)}"><a class="nav-link" href="${sphinx_parent.get('link')}">${sphinx_parent.get('title')}</a></li>
	          ## <li class="nav-item nav-item-${parents.index(sphinx_parent)}"><a href="${parent.link}">${parent.title}</a>
	        % endfor
	      </ul>
		</div>
	  </div>
	</nav>
</%def>

<%def name="render_sidebar()">
  <div id="sidebar">
    ## <div class="sphinxsidebar" role="navigation" aria-label="main navigation">
      ## <div class="sphinxsidebarwrapper">
        % if logo is not UNDEFINED and logo:
          ## <p class="logo">
		  ##   <a href="${pathto(master_doc)}">
          ##     <img class="logo" src="${pathto('_static/' + logo, 1)}" alt="Logo"/>
          ##   </a>
		  ## </p>
		  <li class="nav-item">
		    <a class="nav-link">
			  <img class="logo" src="${pathto('_static/' + logo, 1)}" alt="Logo"/>
			</a>
		  </li>
		% endif

        <%doc>
		Sphinx wants you to include the sidebars you want in your page as part of the conf.py in the source directory.
		Alongside this, there are a few "builtin" sidebar templates that can be rendered:
		  * localtoc.html - a fine-grained table of contents of the current document
		  * globaltoc.html - a coarse-grained table of contents for the whole documentation set, collapsed
		  * relations.html - two links to the previous and next documents
		  * sourcelink.html - a link to the source of the current document, if enabled in ``html_show_sourcelink``
		  * searchbox.html - the "quick search" box

		They made a conscious decision moving away from blocked-sidebars, and prefer that sidebars be included dynamically like this.

		For now, they'll remain as part of this block, but ideally they should be sub-templates.
		</%doc>
		
		## Render each sidebartemplate in ``sidebars``
		% if sidebars is not UNDEFINED and sidebars is not None:
		  % for sidebar in sidebars:
		    ## TODO: Render `sidebar` (which is a str of a sidebar-template's filename)
		  % endfor
		% endif

		## localtoc
		${context.get('toc')}

      ## </div>
    ## </div>
  </div> <!-- class="sidebar" -->
</%def>

<%def name="footer()">
    <div class="footer">
	  % if hasdoc('copyright'):
	    &#169; <a href="${pathto('copyright')}">Copyright</a>
	  % endif

	  % if last_updated is not UNDEFINED and last_updated is not None:
	    Last updated on ${last_updated}
	  % endif

	  % if show_sphinx is not UNDEFINED:
	    <a href="http://sphinx-doc.org/">Sphinx</a> ${sphinx_version}
	  % endif
	</div>
</%def>

<%def name="debug()">
  <div id="debug_modal" class="modal fade" tabindex="-1">
    <div class="modal-dialog">
	  <div class="modal-content">
	    <div class="modal-header">
		  <h1 class="modal-title">Sphinx Context</h1>
		</div>
		<div class="modal-body">
          <ul>
            % for key in sorted(context['pageargs'].keys()):
              % if key == "sphinx_body":
                <li><b>${key}</b>: See the non-debug for the body!</li>
              % else:
                <li><b>${key}</b>: ${context.get(key)}</li>
              % endif
            % endfor
          </ul>
		</div>
	  </div>
	</div>
  </div>
</%def>
