<!DOCTYPE HTML>
<html>

<head>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

  <script>
	// load the empty form
    $(document).ready(function(){
	  $.get("${request.route_url('form')}", function(form_html) {
	    $("#form_div").html(form_html);  
	  });
    });
      
    // set the ajax properties for the form	
	$(document).on('submit', '#form_div form', function(e){
	  e.preventDefault();
	  var form = $("#form_div form");
      $.ajax({
	    type: form.attr('method'),
		url: form.attr('action'),
		data: form.serialize(),
		success: function(data) {
		  location.reload();  // reload whole page
		},
		error: function(jqXHR, textStatus, errorThrown){
		  $("#form_div").html(jqXHR.responseText);  // change form HTML
		}
	  });
	});

  </script>


</head>

<body>
  <h1>Form as a Separate Template</h1>
  % if people:
    <h2>People</h2>
    <ul>
      % for person in people:
        <li>
          ${person['firstname']} ${person['lastname']} - Age: ${person['age']}
      	Phone #: ${person['phone_number']}
        </li>
      % endfor
    </ul>
  % endif

  <div id="form_div">
  </div>
</body>

</html>
