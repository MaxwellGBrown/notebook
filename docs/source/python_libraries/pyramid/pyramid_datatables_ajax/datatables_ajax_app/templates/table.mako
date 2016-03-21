<html>

<head>
<!-- jQuery -->
<script type="text/javascript" charset="utf8" src="//code.jquery.com/jquery-1.10.2.js"></script>

<!-- DataTables CSS -->
<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.7/css/jquery.dataTables.css">
  
<!-- DataTables -->
<script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.7/js/jquery.dataTables.js"></script>

<script type='text/javascript' charset='utf8'>
$(document).ready(function() {

	var url = $(".datatable").data('url');
	$(".datatable").DataTable({
		"ajax": {
			url: url,
			method: "POST",
			data: function(d) {
					return JSON.stringify(d);
				},
			},
	});
	$("#static_datatable").DataTable();
});
</script>
</head>

<body>
	<ul>
		<li>
			<a href='${request.route_url("table", table_type="static")}'>
				Rendered HTML DataTable
			</a>
		</li>
		<li>
			<a href='${request.route_url("table", table_type="ajax")}'>
				Load Table Data via AJAX
			</a>
		</li>
		<li>
			<a href='${request.route_url("table", table_type="server-side")}'>
				Process Table Data Server Side
			</a>
		</li>
	</ul>

	% if table_type == 'static':

	<h1>Static DataTable</h1>
	<p>This DataTable is rendered as an HTML table as part of the page</p>
	<table id="static_datatable">
		<thead>
			<th>Every Other Number</th>
			<th>Positive Numbers</th>
			<th>Negative Numbers</th>
		</thead>

		<tbody>
			% for record in records:
			<tr>
				<td>${record['every_other_number']}</td>
				<td>${record['pos_and_negs']['pos']}</td>
				<td>${record['pos_and_negs']['neg']}</td>
			</tr>
			% endfor
		</tbody>
	</table>


	% elif table_type == "ajax":

	<h1>AJAX Data Load</h1>
	<p>This DataTable makes 1 request to the server upon creation to load all of the table's data. Searching, filtering, and ordering all happens locally.</p>
	<table class="datatable" data-url="${request.route_url('table_data', table_type='ajax')}">
		<thead>
			<tr>
				<th data-data="every_other_number">Every Other Number</th>
				<th data-data="pos_and_negs.pos">Positive Numbers</th>
				<th data-data="pos_and_negs.neg">Negative Numbers</th>
			</tr>
		</thead>
	</table>


	% elif table_type == "server-side":

	<h1>AJAX Server Side Processing</h1>
	<p>This DataTable only sends a new request to the server for every page, sort, and search, and loads the data when received.</p>
	<table class="datatable" data-url="${request.route_url('table_data', table_type='server-side')}" data-server-side="true">
		<thead>
			<tr>
				<th data-data="every_other_number">Every Other Number</th>
				<th data-data="pos_and_negs.pos">Positive Numbers</th>
				<th data-data="pos_and_negs.neg">Negative Numbers</th>
			</tr>
		</thead>
	</table>

	% endif
</body>
</html>
