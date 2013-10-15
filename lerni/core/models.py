# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from lerni.domain.models import Topic
from lerni.domain.models import Page


class Teacher(models.Model):

    user = models.ForeignKey(User)


class StudyContext(models.Model):

    time_current_topic = models.FloatField()
    time_current_page = models.FloatField()
    current_topic = models.ForeignKey(Topic)
    current_page = models.ForeignKey(Page)


class Student(models.Model):

    user = models.ForeignKey(User, null=False)
    level_learning = models.CharField(max_length=200)
    level_learning_theoretical = models.CharField(max_length=200)
    level_learning_pratical = models.CharField(max_length=200)
    study_context = models.OneToOneField(StudyContext)
