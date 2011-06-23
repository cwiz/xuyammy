from models import  Task, Story, Tag, Sprint, Project
from models import get_tags_since, get_stories_since, get_tasks_since
from utils.views import dict_2_json
from datetime import datetime
from tornado.websocket import WebSocketHandler
import time
import tornado

LISTENERS = []

def get_current_items(timestamp=None):
    if timestamp is not None:
        tasks = get_tasks_since(timestamp)
        stories = get_stories_since(timestamp)
        tags = get_tags_since(timestamp)

    else:
        tasks = Task.objects.all()
        stories = Story.objects.all()
        tags = Tag.objects.all()

    return dict_2_json({
        'status': 'success',
        'tasks': tasks.values(),
        'stories': stories.values(),
        'tags': tags.values(),
        'timestamp': time.time()
    })


class WebSocketEventHandler(WebSocketHandler):
    def open(self):
        LISTENERS.append(self)


    def on_message(self, message):
        pass


    def on_close(self):
        if self in LISTENERS:
            LISTENERS.remove(self)


def update_clients(data):
    for element in LISTENERS:
        element.write_message(data)


class RESTHandler(tornado.web.RequestHandler):
    def __fill_object_from_request(self, obj):

        for attribute in obj.__dict__.copy().keys():

            if attribute in self.request.arguments:
                new_value = self.get_argument(attribute)

                if new_value:
                    setattr(obj, attribute, new_value)

        obj.save()
        

    def post(self, *args, **kwargs):
        if 'id' in self.request.arguments: # update scenario
            obj = self.cls.get(self.get_argument('id'))
            self.__fill_object_from_request(obj)

        else: # create scenario
            print self.request.arguments
            obj = self.cls()
            self.__fill_object_from_request(obj)

        current_items = get_current_items(datetime.now())
        update_clients(current_items)
        return self.write(current_items)


    def delete(self, *args, **kwargs):
        if 'id' in self.request.arguments:
            self.cls.objects.filter(id=self.request.get_argument('id')).delete()

    def get(self, *args, **kwargs):
        self.write(str(self.cls))


class MainDashboardHandler(tornado.web.RequestHandler):
    def get(self):
        html = open('static/index.html').read()
        self.write(html)


class AjaxDashboardHandler(tornado.web.RequestHandler):
    def get(self):
        timestamp = datetime.fromtimestamp(
            float(self.get_argument('timestamp'))) if 'timestamp' in self.request.arguments else None
        return self.write(get_current_items(timestamp))


class StoryHandler(RESTHandler):
    cls = Story


class TaskHandler(RESTHandler):
    cls = Task


class TagHandler(RESTHandler):
    cls = Tag


class SprintHandler(RESTHandler):
    cls = Sprint


class ProjectHandler(RESTHandler):
    cls = Project




