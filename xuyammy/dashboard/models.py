# -*- coding: utf-8 -*-

from django.db import models

class Project(models.Model):
    name = models.TextField(max_length=200)
    description = models.TextField(max_length=500)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    deleted = models.BooleanField(default=False)


class Sprint(models.Model):
    start_date = models.DateField()
    name = models.TextField(max_length=200)
    description = models.TextField(max_length=500)
    project = models.ForeignKey(Project)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    deleted = models.BooleanField(default=False)


class Story(models.Model):
    """This is basicaly a User Story, that contains a number of Tasks leading to the successful Story implementation"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    weight = models.IntegerField(blank=True, null=True)
    sprint = models.ForeignKey(Sprint, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    deleted = models.BooleanField(default=False)


class Tag(models.Model):
    """Tag is almost any attribute of any object"""
    name = models.CharField(max_length=140)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    deleted = models.BooleanField(default=False)


class Task(models.Model):
    """This is a task that contains all task fields such as description, creation time, etc"""

    OPEN = 1
    IN_PROGRESS = 2
    DONE = 3
    ARCHIVED = 4

    STATUS_CHOICES = (
    (OPEN, 'Open'),
    (IN_PROGRESS, 'In progress'),
    (DONE, 'Done'),
    (ARCHIVED, 'Archived'),
    )

    description = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN)
    story = models.ForeignKey(Story)
    tags = models.ManyToManyField(Tag, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=True)
    deleted = models.BooleanField(default=False)


def get_tasks_since(date):
    return Task.objects.filter(updated__gte=date)


def get_stories_since(timestamp):
    return Story.objects.filter(updated__gte=timestamp)


def get_tags_since(timestamp):
    return Tag.objects.filter(updated__gte=timestamp)