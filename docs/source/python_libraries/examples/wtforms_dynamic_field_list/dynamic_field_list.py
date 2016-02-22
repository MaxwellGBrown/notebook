import wtforms
from wtforms.widgets import html_params, HTMLString


class DynamicFieldList(wtforms.fields.FieldList):
    def __init__(self, unbound_field, *args, **kwargs):
        super().__init__(unbound_field, *args, **kwargs)
        self.widget = add_field_widget_wrapper(self.widget)

    def _add_entry(self, *args, **kwargs):
        field = super()._add_entry(*args, **kwargs)
        field.widget = deleteable_widget_wrapper(field.widget)


def deleteable_widget_wrapper(widget):
    """
    Wraps widget in div w/ a link to delete div & it's wrapped widget
    """
    def _deleteable_widget(field, **kwargs):
        html_string = "<div>"
        html_string += widget(field, **kwargs)
        link_param_kwargs = {
                "onclick": "$(this).parent().remove();",
                "href": "javascript:void(0)",
                }
        link_params = html_params(**link_param_kwargs)
        html_string += "<a {}>Delete</a>".format(link_params)
        html_string += "</div>"
        return HTMLString(html_string)
    return _deleteable_widget


def add_field_widget_wrapper(widget):
    """
    Wraps all subfields in a div, adds a link to append subfields to that div.
    """
    def _add_field_widget(field, **kwargs):
        # spoof field_name in context of it's form
        field_name = "{}{}".format(
                field._prefix,
                field.short_name,
                )

        # render child fields (which should be wrapped w/ delete widgets)
        wrapper_id = "{}_wrapper".format(field_name)
        html_string = "<div {}>".format(html_params(id=wrapper_id))
        for subfield in field:
            html_string += subfield.widget(subfield, **kwargs)
        html_string += "</div>"

        # render a hidden template of the subfields 
        template_id = "{}_template".format(field_name)
        subform_tmpl_kwargs = {
                "id": template_id,
                "style": "display: none;",
                }
        html_string += "<div {}>".format(html_params(**subform_tmpl_kwargs))
        tmpl_prefix = "{0}-!{0}!".format(field_name)
        tmpl_field = field.unbound_field.bind(form=None, name=tmpl_prefix,
                prefix="", _meta=field.meta)
        tmpl_field.process(formdata=None, data={})
        tmpl_field.widget = deleteable_widget_wrapper(tmpl_field.widget)
        html_string += tmpl_field.widget(tmpl_field)
        html_string += "</div>"

        # create function that duplicates the template field
        field_name_regex = field_name.replace("-", "\-").replace("_", "\_")
        tmpl_regex = "\!+{0}+\!".format(field_name_regex)
        onclick = """
$("#{0}").append(
    $("#{1}").clone()  // Duplicate subform from template
    .show()  // Display the duplicated subform
    .html(  // rewrite HTML of new subform
        $('#{1}').html()
            .replace(new RegExp('{2}', 'g'),
                        (new Date).getTime().toString())
         )
    .attr('id', '')  // remove #subform_template from new subform
);""".format(wrapper_id, template_id, tmpl_regex)
        new_link_params = html_params(
                href="javascript:void(0)",
                onclick=onclick,
                )
        html_string += "<a {}>".format(new_link_params)
        html_string += "New"
        html_string += "</a>"
        return HTMLString(html_string)
    return _add_field_widget


