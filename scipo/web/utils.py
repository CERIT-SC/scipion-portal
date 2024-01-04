
import re

from django.shortcuts import render
from django.contrib import messages

def parse_number_with_unit(input_string):
    # Define a regular expression pattern to match the numeric value and unit
    # E.g. "256Gi"
    pattern = re.compile(r'(\d+)([A-Za-z]*)')
    match = pattern.search(input_string)

    if match:
        # Extract the numeric value and unit from the match groups
        value = int(match.group(1))
        unit = match.group(2)

        return {"value": value, "unit": unit}
    else:
        return {}


def _messages_payload(request):
    """
    Solves the problem with adding additional data to the django messages.
    """
    messages_extra_tags = list()

    msgs = messages.get_messages(request)
    if msgs:
        for msg in msgs:
            extra_tags = ""

            if   msg.tags == "debug":
                extra_tags = { "title": "Debug",   "html_class": "alert-info",    "fa": "fa-bug" }
            elif msg.tags == "info":
                extra_tags = { "title": "Info",    "html_class": "alert-info",    "fa": "fa-info" }
            elif msg.tags == "success":
                extra_tags = { "title": "Success", "html_class": "alert-success", "fa": "fa-check" }
            elif msg.tags == "warning":
                extra_tags = { "title": "Warning", "html_class": "alert-warning", "fa": "fa-exclamation-triangle" }
            elif msg.tags == "error":
                extra_tags = { "title": "Error",   "html_class": "alert-danger",  "fa": "fa-ban" }

            messages_extra_tags.append({
                "message": msg,
                "extra_tags": extra_tags
            })

    return messages_extra_tags

def scipo_render(
    request,
    template_name,
    context = None,
    content_type = None,
    status = None,
    using = None
):
    """
    Custom proxy function of the basic "render()" with additional payload on the "context".
    """

    if context:
        context.update({
            "messages_extra_tags": _messages_payload(request)
        })

    return render(
        request,
        template_name,
        context,
        content_type,
        status,
        using
    )
