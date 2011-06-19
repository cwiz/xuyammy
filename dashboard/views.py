from models import Story, Tag, Task
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
import json
import datetime

from django.core.exceptions import ObjectDoesNotExist
 
 
def index(request):
	return render(request, 'index.html')

def data(request):
    return render(request, 'data.html', {
        'tasks' :   serialize_model(Task),
        'stories' : serialize_model(Story),
        'tags' :    serialize_model(Tag),
        'timestamp' : datetime.now(),
    })

def add_task(request):
    try:
    # get related story 
        s = Story.objects.get(id=request.GET['story_id'])
        # create task object 
        t = Task(description=request.GET['description'], story=s)
        t.save()

        # now log addition
        LogEntry.objects.log_action(
            user_id         = request.user.pk, 
            content_type_id = ContentType.objects.get_for_model(t).pk,
            object_id       = t.pk,
            object_repr     = force_unicode(t), 
            action_flag     = ADDITION
        )
        return HttpResponse('{"status" : "Success", "task_id" : t.id }')
    except KeyError:
        return HttpResponse('{"status" : "Fail", "reason" : "Missing some of the required parameters: description, strory_id"}')
    except DoesNotExist:
        return HttpResponse('{"status" : "Fail", "reason" : "It seems story_id is pointing on the non-existent story"}')
        
    return render(request, 'index.html')
    
def update(request):
    try:
        # trying to get all objects changed/added since timestamp
        entries = LogEntry.objects.select_related('object_repr').filter(action_time__gt=datetime.datetime.fromtimestamp(int(request.GET['timestamp'])))
        for entry in entries:
            print entry.object_repr
            
        return HttpResponse('{"status" : "Success"}')
    except KeyError:
        return HttpResponse('{"status" : "Fail", "reason" : "Missing timestamp GET parameter"}')
        
        
def serialize_model(model):
    result = {}
    for item in model.objects.values():
        result[item['id']] = item
    return json.dumps(result, cls=DjangoJSONEncoder, indent=4)