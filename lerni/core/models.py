# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from lerni.domain.models import Topic
from lerni.domain.models import Page


class Teacher(models.Model):

    user = models.ForeignKey(User)


class StudyContext(models.Model):

    current_topic = models.ForeignKey(Topic)
    current_page = models.ForeignKey(Page)


class Grades(models.Model):

    topic = models.ForeignKey(Topic)
    grade_teoretical = models.SmallIntegerField(_(u'nota teórica'))
    grade_pratical = models.SmallIntegerField(_(u'nota prática'))
    grade_final = models.SmallIntegerField(_(u'nota final'))
    grade_fuzzy_teoretical = models.SmallIntegerField(_(u'nota fuzzy teórica'))
    grade_fuzzy_pratical = models.SmallIntegerField(_(u'nota fuzzy prática'))
    grade_fuzzy_final = models.SmallIntegerField(_(u'nota fuzzy final'))


class Student(models.Model):

    user = models.ForeignKey(User, null=False)
    level_learning = models.CharField(max_length=200)
    level_learning_theoretical = models.CharField(max_length=200)
    level_learning_pratical = models.CharField(max_length=200)
    study_context = models.OneToOneField(StudyContext)
    grade = models.ForeignKey(Grades, null=False)
