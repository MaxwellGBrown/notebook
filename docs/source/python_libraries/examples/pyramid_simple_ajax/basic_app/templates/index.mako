<html>
<head>
    <title>Simple Ajax</title>

  <!-- jQuery -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js">
  </script>

  <!-- Bootstrap -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
</head>

<body>
<div class="container">

<h1 class="text-center">Simple Ajax</h1>

<div class="progress">
  <div id="progress_bar" class="progress-bar" role="progressbar" style="width: 0%">
    0%
  </div>
</div>

<form id="simple_ajax_form" action="${request.route_url('ajax_process')}" method="POST">
  <p class='help-block'>Count using the range function via ajax_process</p>
  <div class="form-group">
    <fieldset id="simple_ajax_form_fields">
      <ul class='list-unstyled'>
        <li>
          Start at: <input type="text" class="form-control" name="start">
        </li>
        <li>
          End at: <input type="text" class="form-control" name="end">
        </li>
        <li>
          Count by: <input type="text" class='form-control' name="step">
        </li>
        <li>
          <input type="submit" class="btn btn-default" value="Run Ajax Process">
        </li>
      </ul>
    </fieldset>
  </div>
</form>
</div>

<script>

// run simple_ajax(event) when form is submitted
$(document).on("submit", "#simple_ajax_form", function(event) {
  event.preventDefault();  // stop plain submit; this is overriding it

  $("#progress_bar").removeClass("progress-bar-success progress-bar-danger");
  $("#progress_bar").attr("style", "width: 0%;");
  $("#progress_bar").text("0%");

  form_url = $("#simple_ajax_form").attr("action");
  form_method = $("#simple_ajax_form").attr("method");
  form_data = $("#simple_ajax_form").serialize();
  // while process is running, disable form for multiple submissions/changes
  $("#simple_ajax_form_fields").attr("disabled", "disabled");

  var send_request = function(){
    console.log("sending ajax request");
    jQuery.ajax({
      type: form_method,
      url: form_url,
      dataType: "json",
      data: form_data,
      success: function(result, textStatus, jqXHR) { 
        percentage_str = result.percentage.toString() + "%";
        console.log("process is " + result.percentage_str + " done");
        $("#progress_bar").text(percentage_str);
      $("#progress_bar").attr("style", "width: " + percentage_str + ";");
      if (result.percentage < 100.0){
        console.log("not finished. sending another request");
        send_request();
      }
      else {
      console.log("process is finished!");
        $("#progress_bar").addClass("progress-bar-success");
        $("#simple_ajax_form_fields").removeAttr("disabled");
      }
      },
      error: function(xhr, ajaxOptions, thrownError){
      console.log("process had an error :(");
        $("#progress_bar").addClass("progress-bar-danger");
        $("#simple_ajax_form_fields").removeAttr("disabled");
      }
    });
  }

  // start the recursion loop
  console.log("Starting the process!");
  send_request();
});



</script>

</body>
</html>
