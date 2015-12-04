<HTML>

<head>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js">
  </script>
  
  <script>
  var tag_count = ${len(form.tags.entries)}
  var addForm = function() {
    <% t_form = child_form(prefix="tags-X-") %>
    new_prefix = "tags-" + tag_count + "-";
    
    form_container = $("#tag_forms");
    form_container.append('<p>Child #' + tag_count + "</p>");
    new_form = '${literal(t_form.tag.label)} ';
    new_form = new_form + '${literal(t_form.tag())}';
    new_form = new_form.split("tags-X-").join(new_prefix);
    form_container.append(new_form);
    tag_count += 1;
  };
  </script>
</head>


<body>
<form method="POST" action="/">
  <div>
    ${form.name.label}: ${form.name()}
  </div>
  
  <div id="tag_forms">
    <% tag_count = 0 %>
    % for entry in form.tags.entries:
      <p>Child #${tag_count}</p>
      ${entry.tag.label}
      ${entry.tag()}
      <% tag_count += 1 %>
    % endfor
  </div>
  
  <div>
    <a href="javascript:void(0)" onclick="addForm()">
      Add Tag
    </a>
  </div>
  
  <input type="submit" name="submit" value="submit" />
</form>
</body>

</HTML>
