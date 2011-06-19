# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Story(models.Model):
    """This is basicaly a User Story, that contains a number of Tasks leading to the successfull Story implementation"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    weight = models.IntegerField(blank=True, null=True)

class Tag(models.Model):
    """Tag is almost any attribute of any object"""
    name = models.CharField(max_length=100)

class Task(models.Model):
    """This is a task that contains all task fields such as description, created time, etc"""

    OPEN = 1
    INPROGRESS = 2
    DONE = 3
    ARCHIVED = 4
    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (INPROGRESS, 'In progress'),
        (DONE, 'Done'),
        (ARCHIVED, 'Archived'),
    )

    description = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=True)

    story = models.ForeignKey(Story)
    tags = models.ManyToManyField(Tag, blank=True)

