from dashboard.handlers import MainDashboardHandler
from dashboard.handlers import AjaxDashboardHandler
from dashboard.handlers import StoryHandler
from dashboard.handlers import TaskHandler

ROUTES = [
    (r"/", MainDashboardHandler),
    (r"/data/", AjaxDashboardHandler),
    (r"/story/", StoryHandler),
    (r"/task/", TaskHandler),
]