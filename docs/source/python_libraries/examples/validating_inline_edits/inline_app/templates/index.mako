<html>
<head>
    <title>Validating Inline Edits Example</title>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

	<script src="${request.static_url('inline_app:static/poshytip-1.2/src/jquery.poshytip.js')}"></script>
	<link href="${request.static_url('inline_app:static/poshytip-1.2/src/tip-yellowsimple/tip-yellowsimple.css')}" rel="stylesheet" />

	<link href="${request.static_url('inline_app:static/jquery-editable/css/jquery-editable.css')}" rel="stylesheet"/>
	<script src="${request.static_url('inline_app:static/jquery-editable/js/jquery-editable-poshytip.min.js')}"></script>

	<script>
		$(document).ready(function() {
			$(".editable").editable({
					"url": "${request.route_url('inline_edit')}",
			});
		});
	</script>
</head>
<body>
<div>
	<h1>WTForms - Validating Inline Edits w/ X-Editable</h1>

	<h2>New Name Form</h2>
		<form action="${request.route_url('index')}" method="POST">
			${form.fullname.label} - ${form.fullname(placeholder='fullname')}
			% if form.fullname.errors:
				<ul>
					% for error in form.fullname.errors:
						<li>${error}</li>
					% endfor
				</ul>
			% endif
			<br>

			${form.nickname.label} - ${form.nickname(placeholder='nickname')}
			<br>
			<input type='submit' value='submit'>
		</form>

	<h2>Inline Edit Current Names</h2>
		<table>
			<thead>
				<tr>
					<td>id</td>
					<td>Fullname</td>
					<td>Nickname</td>
				</tr>
			</thead>
			<tbody>
				% for idx in range(1, len(names.keys()) + 1):
					<% name = names[idx] %>
					<tr>
						<td>${idx}</td>
						<td>
							<a href='#' class='editable' data-pk='${name.id}' data-name='fullname'>
								${name.fullname}
							</a>
						</td>
						<td>
							<a href='#' class='editable' data-pk='${name.id}' data-name='nickname'>
								${name.nickname}
							</a>
						</td>
					</tr>
				% endfor
			</tbody>
		</table>
</div>
</body>
</html>
