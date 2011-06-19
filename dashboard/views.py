from models import Story, Tag, Task
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
import json
import datetime
import time

from django.core.exceptions import ObjectDoesNotExist
 
 
def index(request):
	return render(request, 'index.html')

def data(request):
    if 'timestamp' in request.GET:
        try:
            # trying to get all objects changed/added since timestamp
            entries = LogEntry.objects.filter(
                action_time__gt = datetime.datetime.fromtimestamp(int(request.GET['timestamp'])),
            )
            result = {'tasks' : {}, 'stories' : {}, 'tags' : {}, 'timestamp' : time.time()}
            for e in entries:
                try:
                    obj = e.get_edited_object()
                except ObjectDoesNotExist:
                    continue
                if isinstance(obj, Task):
                    result['tasks'][obj.id] = json.dumps(model_to_dict(obj), cls=DjangoJSONEncoder, indent=4)
                elif isinstance(obj, Story):
                    result['stories'][obj.id] = json.dumps(model_to_dict(obj), cls=DjangoJSONEncoder, indent=4)
                elif isinstance(obj, Tag):
                    result['tags'][obj.id] = json.dumps(model_to_dict(obj), cls=DjangoJSONEncoder, indent=4)

            return render(request, 'data.html', result)

        except KeyError:
            return HttpResponse('{"status" : "Fail", "reason" : "Missing timestamp GET parameter"}')
    else:
        return render(request, 'data.html', {
            'tasks' :   serialize_model(Task),
            'stories' : serialize_model(Story),
            'tags' :    serialize_model(Tag),
            'timestamp' : time.time(),
        })

def task_save(request):

    # update or create
    if 'id' in request.GET:
        t = Task.objects.get(id=request.GET['id'])
        for attr in t.__dict__.copy():
            if request.GET.get(attr):
                setattr(t, attr, request.GET.get(attr))
        
        t.save()
        flag = CHANGE
    else:
        try:
        # get related story 
            s = Story.objects.get(id=request.GET['story_id'])
            # create task object 
            t = Task(description=request.GET['description'], story=s)
            t.save()
            flag = ADDITION

        except KeyError:
            return HttpResponse('{"status" : "Fail", "reason" : "Missing some of the required parameters: description, strory_id"}')
        except DoesNotExist:
            return HttpResponse('{"status" : "Fail", "reason" : "It seems story_id is pointing on the non-existent story"}')

        
    # now log addition or update
    LogEntry.objects.log_action(
        user_id         = request.user.pk, 
        content_type_id = ContentType.objects.get_for_model(t).pk,
        object_id       = t.pk,
        object_repr     = force_unicode(t), 
        action_flag     = flag
    )
    
    task_json = json.dumps(model_to_dict(t), cls=DjangoJSONEncoder, indent=4)
    
    return HttpResponse('{"status" : "Success", "task" : %s }' % (task_json))
    
        
def serialize_model(model):
    result = {}
    for item in model.objects.values():
        result[item['id']] = item
    return json.dumps(result, cls=DjangoJSONEncoder, indent=4)
    