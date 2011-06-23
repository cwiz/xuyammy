from dashboard.handlers import MainDashboardHandler
from dashboard.handlers import AjaxDashboardHandler
from dashboard.handlers import StoryHandler
from dashboard.handlers import TaskHandler
from dashboard.handlers import WebSocketEventHandler
from dashboard.handlers import TagHandler
from dashboard.handlers import SprintHandler
from dashboard.handlers import ProjectHandler

ROUTES = [
    # REST guys
    (r"/project/", ProjectHandler),
    (r"/sprint/", SprintHandler),
    (r"/story/", StoryHandler),
    (r"/task/", TaskHandler),
    (r"/tag/", TagHandler),

    # Other stuff
    (r"/", MainDashboardHandler),
    (r"/data/", AjaxDashboardHandler),
    (r"/ws/", WebSocketEventHandler),
]