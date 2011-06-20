from django.http import HttpResponse
from django.template.base import Template
from django.template.context import Context
import jsonpickle

def json_response(obj):
    return HttpResponse(jsonpickle.encode(value=obj, unpicklable=False), mimetype='application/json')

def render_template(template, context={}):
    t = Template(open(template).read())
    return t.render(Context(context))