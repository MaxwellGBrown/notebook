<HTML>

<head>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js">
  </script>

  <script>
  SUBFORM_ID = 0;
  var insertSubform = function(parent_selector, template_subform_selector) {
    var subform_id_str = "subform_id_" + SUBFORM_ID.toString();
	var new_subform = $("<div/>");
	new_subform.attr('id', subform_id_str);
	new_subform.html($(template_subform_selector.html());
	new_subform.append("<br>");

	new_subform.data('prefix', $(template_subform_selector.data('prefix'));

	var subform_delete = $("<a/>");
	subform_delete.addClass("subform_delete");
	subform_delete.attr("href", "javascript:void(0)");
	var subform_delete_onclick = 'deleteSubform("' + subform_id_str + '")';
	subform_delete.attr("onclick", subform_delete_onclick);
	subform_delete.text("Delete");
	new_subform.append(subform_delete);

	assignSubformIndexes(parent_selector);
	SUBFORM_ID++;
  };

  var deleteSubform = function(subform_id) {
    var subform = $("#" + subform_id);
    var subform_parent = subform.parent();
	subform.remove();
	assignSubformIndexes();
  };

  var assignSubformIndexes = function() {};

  };
  </script>
</head>


<body>
<form method="POST" action="/">
  <div>
    ${form.name.label}: ${form.name()}
  </div>
  
  <div id="tag_forms">
	<div id="subform_template" prefix="${tag_form._prefix}" style="display: none;">
		${tag_form.tag.label}
		${tag_form.tag(placeholder="Tag")}
	</div>

    % for entry in form.tags.entries:
	  <div class="subform">
      	${entry.tag.label}
      	${entry.tag()}
	  </div>
    % endfor
  </div>
  
  <div>
    <a href="javascript:void(0)" onclick="insertSubform('')">
      Add Tag
    </a>
  </div>
  
  <input type="submit" name="submit" value="submit" />
</form>
</body>

</HTML>
