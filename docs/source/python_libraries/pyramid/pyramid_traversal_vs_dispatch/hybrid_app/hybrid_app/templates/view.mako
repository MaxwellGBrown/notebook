<html>
<head>
    <title>${self.title()}</title>
</head>
<body>
<div>
    <h1>${self.title()}</h1>
	${self.body()}
</div>
</body>
</html>


<%def name="title()">
  % if request.context.__name__ is not None:
    ${request.context.__name__}
  % else:
    FooFactory (__name__ is None)
  % endif
</%def>


<%def name="body()">
  <h2>request.context: ${request.context.__repr__()}</h2>
  % if request.context is not None:
    <p>
      <b>__name__</b>: ${request.context.__name__} <br />
      % if request.context.__parent__ is not None:
        <b>__parent__</b>:
		% if request.context.__parent__.__name__ is not None:
		  <a href="${request.resource_url(request.context.__parent__,
		  route_name='view')}">
		    ${request.context.__parent__.__name__ or repr(request.context.__parent__)}
		  </a>
		% else:
		  <a href="${request.resource_url(request.context.__parent__,
		  route_name='view')}">
		    ${request.context.__parent__.__repr__()}
		  </a>
		% endif
		<br />
      % else:
	    <b>__parent__</b>: None<br />
      % endif
    </p>
  % else:
    <p>
	  request.context is None
	</p>
  % endif

  % if hasattr(request.context, '__getitem__'):
    <h2>Add Child</h2>
	% if str(type(request.context)).find("FooFactory") > -1:
      <form action="${request.route_url('new_foo')}" method="POST">
	% elif str(type(request.context)).find("Foo") > -1:
      <form action="${request.route_url('new_bar', foo_name=request.context.foo_name)}" method="POST">
	% elif str(type(request.context)).find("Bar") > -1:
      <form action="${request.route_url(route_name='new_baz', foo_name=request.context.foo_name, bar_name=request.context.bar_name)}" method="POST">
	% else:
      <form action="${request.route_url(route_name='new_qux', foo_name=request.context.foo_name, bar_name=request.context.bar_name, baz_name=request.context.baz_name)}" method="POST">
	% endif
      <input name="name" placeholder="name"/>
      <input type="submit"/>
    </form>
  % else:
    <h2>Leaf Resource</h2>
	<p>
	This is a "leaf resource" and, as such, is the end of the resource tree.
	It can not have children resources.
	</p>
  % endif

  % if hasattr(request.context, '__getitem__'):
    <h2>Children</h2>
    ${list_children(request.context)}
  % endif

</%def>

<%def name="list_children(parent)">
  <ul>
    % for child in parent.children():
	  <li>
	    <a href="${request.resource_url(child, route_name='view')}">
		  ${child.__name__}
		</a>
		${list_children(child)}
	  </li>
	% endfor
  </ul>
</%def>
