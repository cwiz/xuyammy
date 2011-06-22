from models import  Task, Story, Tag
from models import get_tags_since, get_stories_since, get_tasks_since
from utils.views import dict_2_json

from datetime import datetime

import time
import tornado

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


class MainDashboardHandler(tornado.web.RequestHandler):
    def get(self):
        html = open('static/index.html').read()
        self.write(html)


class AjaxDashboardHandler(tornado.web.RequestHandler):
    def get(self):
        timestamp = datetime.fromtimestamp(
            float(self.get_argument("timestamp"))) if 'timestamp' in self.request.arguments else None
        return self.write(get_current_items(timestamp))


class StoryHandler(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument('name')
        Story.objects.get_or_create(name=name)

        return self.write(get_current_items())


class TaskHandler(tornado.web.RequestHandler):
    def post(self):
        if 'id' in self.request.arguments:
            id = self.get_argument('id')
            task = Task.objects.get(id)

            for attribute in task.__dict__.copy():
                if self.request.arguments.get(attribute):
                    setattr(task, attribute, self.request.arguments.get(attribute))

            task.save()
            return self.write(dict_2_json({
                'status': 'success',
                'tasks': [task]
            }))

        if 'story_id' in self.request.arguments:
            story_id = self.get_argument("story_id")
            description = self.get_argument('description')
            try:
                task = Task(description=description, story_id=story_id)
                task.save()

            except KeyError:
                return dict_2_json({
                    'status': 'fail',
                    'errors': ['Missing some of the required parameters: description, story_id']
                })

            except Task.DoesNotExist:
                return dict_2_json({
                    'status': 'fail',
                    'errors': ['It seems story_id is pointing on the non-existent story']
                })

        return self.write(get_current_items())



