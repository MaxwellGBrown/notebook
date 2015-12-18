import json

from pyramid.response import Response
from pyramid.view import view_config


records = [
        {
            "every_other_number": i * 2,
            "pos_and_negs": {"pos": i, "neg": i * -1}
        }
        for i in range(1, 101)
        ]


@view_config(route_name='table', renderer='templates/table.mako')
def table(request):
    table_type = request.matchdict['table_type']
    return dict(table_type=table_type, records=records)


@view_config(route_name='table_data')
def table_data(request):
    table_type = request.matchdict['table_type']
    # decode request.body's json object
    decoder = json.JSONDecoder()
    data_request = decoder.decode(request.body)

    print_data_request(data_request)  # for example logging

    data_fxn = get_data if table_type == "server-side" else all_data
    data = data_fxn(data_request)
    response_dict = {
            "draw": data_request.get('draw') or "",  # request/response id
            "recordsTotal": 100,  # all records in record set
            "recordsFiltered": 100,  # records in total that match filter
            "data": data,  # data to be applied to table
            }
    json_table_data = json.dumps(response_dict)
    return Response(json_table_data)


def get_data(data_request):
    """
    Returns an object to be json.dump()'d to a DataTable.

    Handles server-side AJAX paging/sorting/searching.
    """
    # "query" the "database" for the data (and format it for the response)
    data = list()
    start, length = data_request['start'], data_request['length']
    for idx in range(start, start + length):
        record = records[idx]
        row_data = {
                # <tr data-row_id="idx">
                "DT_RowAttr": {"data-row_id": idx},
                "every_other_number": record['every_other_number'],
                # json.dumps converts dicts into objects.
                # e.g. record['pos_and_negs']['pos'] -> pos_and_negs.pos
                "pos_and_negs": record['pos_and_negs'],
                }
        data.append(row_data)
    return data


def all_data(data_request):
    """
    Returns an object to be json.dump()'d to a DataTable.

    For AJAX table loading that takes the data up front.
    """
    data = list()
    row_id = 1
    for record in records:
        row_data = {
                "DT_RowAttr": {'data-row_id': row_id},
                "every_other_number": record['every_other_number'],
                # json.dumps converts dicts into objects.
                # e.g. record['pos_and_negs']['pos'] -> pos_and_negs.pos
                "pos_and_negs": record['pos_and_negs'],
                }
        data.append(row_data)
        row_id += 1
    return data


def print_data_request(data_request):
    print("\n{:^79}\n{:-^79}".format("DataTables request.body", ""))
    for key in data_request:
        if key != "columns":
            print("{}: {}".format(key, data_request[key]))
        else:
            print("columns:")
            for col_idx in range(len(data_request[key])):
                print("  {}: {}".format(col_idx, data_request[key][col_idx]))
    print("{:-^79}\n".format(""))
