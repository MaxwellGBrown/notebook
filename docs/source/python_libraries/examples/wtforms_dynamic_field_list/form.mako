<HTML>

<head>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js">
  </script>
</head>


<body>
<form method="POST" action="/">

  <h1>DynamicParentField Demo</h1>
  <p>This form houses two DynamicParentFields, <b>primary_tags</b> and <b>secondary_tags</b>.</p>
  
  <h2>primary_tags</h2>
  ${form.primary_tags()}
  <h2>secondary_tags</h2>
  ${form.secondary_tags()}
  
  <br/>
  <input type="submit" name="submit" value="submit" />
</form>
</body>

</HTML>
