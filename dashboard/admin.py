from django.contrib import admin
from dashboard.models import Task, Tag, Story

admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(Story)