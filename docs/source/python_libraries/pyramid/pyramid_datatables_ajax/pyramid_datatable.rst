=========================
AJAX DataTables & Pyramid
=========================

**can be found in** ``exaples/pyramid_datatables_ajax/``

DataTables is a jQuery package that creates neat, clean, and sexy tables that
can have their functionality extended with minimal effort (...sometimes).

One of the advantages that DataTables can provide is the ability to load data
via AJAX.

This example outlines the basic initialization of DataTables, and how to work
with AJAX DataTables data in Pyramid.


----------------------------------
Loading DataTables & prerequisites
----------------------------------

To begin, the table must be loaded via CDN. 

.. code-block:: html

    <!-- jQuery -->
    <script type="text/javascript" charset="utf8" src="//code.jquery.com/jquery-1.10.2.js"></script>
    
    <!-- DataTables CSS -->
    <link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.7/css/jquery.dataTables.css">
      
    <!-- DataTables -->
    <script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.7/js/jquery.dataTables.js"></script>


--------------------------
Initializing the DataTable
--------------------------

Initializing a DataTable is as easy as calling ``.DataTable({})`` on a jQuery table selected object.

A DataTable can take initializing arguments from the JSON object on
itialization (e.g. ``.DataTable({processing: true}))``) or as part of the
table's ``data-*`` attributes (e.g. ``<table data-processing=true>``).

Here's a `complete list of DataTables initializaiton arguments <http://datatables.net/reference/option/>`_.

.. note::

   Any initialization arguments in 'camelCase' are replaced with dashed strings for data-* values!

   (e.g. serverSide -> data-server-side)


Here is how a simple AJAX DataTable is initialized in the example:

.. code-block:: javascript

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


In this example, since the ``ajax`` method is a little too complex for a
``data-*`` attribute, the url is loaded from the ``data-url`` attribute instead of definining it in the javascript code.

To complete the DataTable, there just needs to be an HTML Table!

.. code-block:: html

	<table class="datatable" data-url="${request.route_url('table_data', table_type='ajax')}">
		<thead>
			<tr>
				<th data-data="every_other_number">Every Other Number</th>
				<th data-data="pos_and_negs.pos">Positive Numbers</th>
				<th data-data="pos_and_negs.neg">Negative Numbers</th>
			</tr>
		</thead>
	</table>


Here, the columns of the DataTable are being defined as ``<th>`` tags (instead of within the table initialization). The ``data-data`` attribute is the part of the JSON row object in the server response where that column gets it's data from.


------------------------------------
Getting Data from the View Callables
------------------------------------

DataTables can take AJAX data as a JS Array or as JSON objects. JSON objects
are nice because the data doesn't have to be in any order, and can include data
that isn't used in the table.

Sending ajax data is quite different depending on if the table has
``serverSide`` enabled or not. Below will outline both methods.

.. note::

   JSON output is matched to a column through that <th> tag's ``data-data``
   attribute, or in the column's initialization in the JS!

   Any time json.dumps() is run, the object is json-ified, and elements can be
   referenced as ``object.attribute`` and ``object['attribute']``!

~~~~~~~~~~~~~~~~~~~~~
Single Load AJAX Data
~~~~~~~~~~~~~~~~~~~~~

Single Load ajax data is the easiest AJAX format to set up. It requires the
reading of no JSON requests, just returning all of the data that is necessary
for the table.

Below is an abbreviated version of the examples "Single Load" ajax table.

.. code-block:: python

    import json
    from pyramid.response import Response
    from pyramid.view import view_config

    @view_config(route_name='table_data')
    def table_data(request):
        data = list()
        for record in records:
            row_data = {
                "DT_RowAttr": {'data-row_id': record.id},
                "every_other_number": record['every_other_number'],
                "pos_and_negs": record['pos_and_negs'],
            }
            data.append(row_data)
        json_dict = {"data": data}
        json_data = json.dumps(json_dict)
        return Response(json_data)


The view callable iterates through every item in the "database" and sets the
values of ``row_data`` which will become a JSON object in ``json.dumps()``. 

After ``$(document).ready()``, the table will send a request to the server and
once all of the data is returned and indexed, the table will display the
values!


After loading the data, the table is essentially treated as a static HTML
table. To get new data from the server either the page needs to be refreshed, or the data needs to be reloaded. Any ordering/paging/filtering is done completely in the browser.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Server Side AJAX Data Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Server side ajax data processing is far more complex than single-loading the
data. All of the "sexy" features of static DataTables now have to be handled by
the server. The following is a non-exhaustive list of things that will send a
request for data to the server:

* Changing pages
* Changing the page size
* Ordering by a column
* Searching/filtering

To keep all of these features enabled, the server has to be able to read the
requests to determine what exactly is being requested and return only the
specific data pertinent to the request. 

Below is the (non-sorting, non-filtering) reading and response to table data.

.. code-block:: python

    @view_config(route_name='table_data')
    def table_data(request):
        decoder = json.JSONDecoder()
        data_request = decoder.decode(request.body)

        # get the table data based off the request
        data = list()
        start, length = data_request.get('start'), data_request.get('length')
        for record in records[start:start + length]:
            row_data = {
                "DT_RowAttr": {"data-row_id": record.id},
                "every_other_number": record['every_other_number'],
                "pos_and_negs": record['pos_and_negs'],
            }
            data.append(row_data)

        response_dict = {
                "draw": data_request['draw'],
                "recordsTotal": len(records),
                # recordsFiltered is the count of records that match the filter
                "recordsFiltered": len(records),
                "data": data,
        }
        json_response = json.dumps(response_dict)
        return Response(json_response)


This example skims over the reading of the JSON request, which contains all of
the information for filtering, sorting, and paging. A typical JSON DataTables
request looks like this:

.. code-block:: javascript

    {
        search: {u'regex': False, u'value': u''},
        draw: 1,
        start: 0,
        length: 10,
        order: [{u'column': 0, u'dir': u'asc'}],
        columns: [
                {
                    u'orderable': True,
                    u'search': {u'regex': False, u'value': u''},
                    u'data': u'every_other_number',
                    u'name': u'',
                    u'searchable': True,
                },
                {
                    u'orderable': True,
                    u'search': {u'regex': False, u'value': u''},
                    u'data': u'pos_and_negs.pos',
                    u'name': u'',
                    u'searchable': True
                },
                {
                    u'orderable': True,
                    u'search': {u'regex': False, u'value': u''},
                    u'data': u'pos_and_negs.neg',
                    u'name': u'',
                    u'searchable': True
                },
        ]
    }


Here's a breakdown of the request and what each of the values means:

search
    The table-wide search function, and associated values.

    search.regex
        Whether or not the search is regex

    search.value
        The value the client has in the search box

draw
    an id pertaining to the data-request. The table is expecting to get a matching draw response value for the request.

start
    the row-number of the first item being displayed in the table

length
    the number of entries visible in the page. The response is expecting this many entries in the data.

order
    Which column the data is being ordered by

    order.column
        the index of the column in this requests ``columns`` that the data is being ordered by

    order.order
        either ``asc`` for ascending or ``desc`` for descending

columns
    a list of columns that data is being requested for, and information about those columns

    columns.orderable
        bool value that says whether the column can be ordered by or not

    columns.search
        column-specific search parameters. operates the same as the table-wide

    columns.data
        the name of the data the column holds (corrosponds to ``data-data``)

    columns.name
        the ``data-name`` of the column

    columns.searchable
        whether or not the column is searchable


The above list is not exhaustive to the data request, but certainly
demonstrates the complexity of a request.

