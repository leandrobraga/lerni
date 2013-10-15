# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField


class Topic(models.Model):

    title = models.CharField(_(u'título'), max_length=200, unique=True)
    position = models.SmallIntegerField(_(u'posição'), unique=True)

    class Meta:

        verbose_name = _(u'tópico')
        verbose_name_plural = _(u'tópicos')
        ordering = ['position']

    def get_total_pages(self):

        return Page.objects.filter(topic=self.id).all().count()

    def __unicode__(self):

        return "%s. %s" % (self.position, self.title)


class Page(models.Model):

    content_page = RichTextField()
    number = models.SmallIntegerField(_(u'número'))
    topic = models.ForeignKey(Topic)

    class Meta:

        verbose_name = _(u'página')
        verbose_name_plural = _(u'páginas')


class Exercise(models.Model):

    LEVEL_CHOICE = ((1, u'Fácil'), (2, u'Médio'), (3, u'Difícil'))
    CORRECT_CHOICE = ((1, 1), (2, 2), (3, 3), (4, 4))
    TIME_CHOICE = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10))
    KIND_CHOICE = ((1, u'Teórico'), (2, u'Prático'))

    question = RichTextField(_(u'questão'), unique=True)
    answer1 = models.CharField(_(u'resposta 1'), max_length=1000)
    answer2 = models.CharField(_(u'resposta 2'), max_length=1000)
    answer3 = models.CharField(_(u'resposta 3'), max_length=1000)
    answer4 = models.CharField(_(u'resposta 4'), max_length=1000)
    correctAnswer = models.SmallIntegerField(_(u'resposta correta'), choices=CORRECT_CHOICE)
    topic = models.ForeignKey(Topic)
    level = models.SmallIntegerField(_(u'nível'), choices=LEVEL_CHOICE)
    time = models.SmallIntegerField(_(u'tempo provável de reposta'), choices=TIME_CHOICE)
    kind = models.SmallIntegerField(_(u'tipo'), choices=KIND_CHOICE)

    class Meta:

        verbose_name = _(u'exercício')
        verbose_name_plural = _(u'exercícios')

