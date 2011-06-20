from models import  Task
from models import get_tags_since, get_stories_since, get_tasks_since
from utils.views import json_response, render_template

import time
import tornado

class MainDashboardHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(render_template('templates/index.html'))


class AjaxDashboardHandler(tornado.web.RequestHandler):
    def post(self):
        id = self.get_argument("id")
        if id is not None:
            task = Task.objects.get(id=request.POST['id'])

            for attribute in task.__dict__.copy():
                if self.request.arguments.POST.get(attribute):
                    setattr(task, attribute, request.POST.get(attribute))

            task.save()
            return self.write(json_response({
                    'status': 'success',
                    'tasks': [task]
            }))

        story_id = self.get_argument("story_id")
        if story_id is not None:
            try:
                task = Task(description=request.POST['description'], story_id=request.POST['story_id'])
                task.save()

            except KeyError:
                return json_response({
                    'status': 'fail',
                    'errors': ['Missing some of the required parameters: description, story_id']
                })

            except Task.DoesNotExist:
                return json_response({
                    'status': 'fail',
                    'errors': ['It seems story_id is pointing on the non-existent story']
                })

    def get(self):

        if 'timestamp' in self.request.arguments:
            timestamp = self.get_argument("timestamp")

            tasks = get_tasks_since(timestamp)
            stories = get_stories_since(timestamp)
            tags = get_tags_since(timestamp)

            response = json_response({
                'status': 'success',
                'tasks': tasks,
                'stories': stories,
                'tags': tags,
                'timestamp': time.time()
            })

            return self.write(response)

        self.write('sdfsdfsd')


