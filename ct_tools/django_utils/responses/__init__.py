from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
import json

def ct_response(content: dict, state=0, content_type="application/json"):
    '''
    @param state : 0-success;1-error;2-login-error
    '''
    data = {
        "data" : content,
        "state" : state
    }
    response = HttpResponse(json.dumps(data), content_type=content_type)
    return response

def response_to_file(file, filename):
    filename = escape_uri_path(filename)
    response = HttpResponse(file, content_type="application/octet-stream")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
