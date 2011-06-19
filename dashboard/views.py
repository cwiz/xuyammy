from models import Story, Tag, Task
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
import json


from django.core.exceptions import ObjectDoesNotExist
 
 
def index(request):
	return render(request, 'index.html')

def data(request):
    return render(request, 'data.html', {
        'tasks' :   serialize_model(Task),
        'stories' : serialize_model(Story),
        'tags' :    serialize_model(Tag),
    })



def serialize_model(model):
    result = {}
    for item in model.objects.values():
        result[item['id']] = item
    return json.dumps(result, cls=DjangoJSONEncoder, indent=4)