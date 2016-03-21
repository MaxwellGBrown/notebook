<form method="POST" action="${request.route_url('form')}">
  <p>${message}</p>

  ${form.firstname.label} - ${form.firstname()}
  % if form.firstname.errors:
    <ul>
	  % for error in form.firstname.errors:
        <li>${error}</li>
	  % endfor
	</ul>
  % endif
  <br/>

  ${form.lastname.label} - ${form.lastname()}
  % if form.lastname.errors:
    <ul>
	  % for error in form.lastname.errors:
        <li>${error}</li>
	  % endfor
	</ul>
  % endif
  <br/>

  ${form.age.label} - ${form.age()}
  % if form.age.errors:
    <ul>
	  % for error in form.age.errors:
        <li>${error}</li>
	  % endfor
	</ul>
  % endif
  <br/>

  ${form.phone_number.label} - ${form.phone_number()}
  % if form.phone_number.errors:
    <ul>
	  % for error in form.phone_number.errors:
        <li>${error}</li>
	  % endfor
	</ul>
  % endif
  <br/>

  <input type="submit" value="submit"/>
</form>
