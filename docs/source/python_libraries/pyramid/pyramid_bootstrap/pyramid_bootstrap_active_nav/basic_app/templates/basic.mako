<html>

<head>
    <title>Pyramid & Bootstrap Active Nav</title>

    <!-- jQuery required for Bootstrap -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    
    <!-- Bootstrap Javascript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
    
    <!-- Bootstrap Styling -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

</head>

<body>
  
<div class="container">

  <h1>Pyramid Bootstrap Auto-Active Navbar</h1>
  
  <br/>

  <ul id="navigation" class="nav nav-pills nav-justified">
    <li><a href="${request.route_url('foo')}">Foo</a></li>
    <li><a href="${request.route_url('bar')}">Bar</a></li>
    <li><a href="${request.route_url('baz')}">Baz</a></li>
  </ul>

  <br/>

  <p class="lead">
    Using some JS, it's easy to automatically detect if the current page
	matches a navbar's link. This can be used to add the "active" class to it.
  </p>

  <pre>
    &lt;script&gt;
      $(document).ready(function(){
        $("#navigation li a").each(function(){
          if ($this).attr('href') == window.location.href){
            $(this).parent().addClass("active"); 
          }
        })
      })
    &lt;/script&gt;
  </pre>

  <div class="alert alert-warning">
    <p>
	  <strong>
	  If your URLs use query strings, some sort of custom-href management needs
	  to be written. The above implementation <em>does not</em> handle query
	  strings.
	  </strong>
	</p>
  </div>

  <script>
    $(document).ready(function(){
      $("#navigation li a").each(function(){
        if($(this).attr('href') == window.location.href){
          $(this).parent().addClass("active");
        };
      })
    });
  </script>

</div>

</body>

</html>
