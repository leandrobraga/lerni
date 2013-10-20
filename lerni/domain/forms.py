# coding: utf-8

from django.forms import ModelForm
from lerni.domain.models import Topic
from lerni.domain.models import Page
from lerni.domain.models import Exercise
from django import forms

import re
from bs4 import BeautifulSoup


class TopicForm(ModelForm):

    class Meta:
        model = Topic


class PageForm(ModelForm):

    class Meta:

        model = Page
        fields = ('content_page', 'number', 'reminder')

    def clean_content_page(self):

        soupContent = BeautifulSoup(self.cleaned_data['content_page'])

        spans = soupContent.findAll('span', style=re.compile('background-color:'))

        cont = 0
        for span in spans:

            if u'background-color:#FFFFFF' == span['style']:

                cont += 1
        if cont == len(spans):
            raise forms.ValidationError(u'O conteúdo da página deve ter um texto em destaque!\n Este texto deve ser uma parte importante do conteúdo para ser reforçada com o aluno!')


        if not re.search('<span style="background-color:', self.cleaned_data['content_page']):

            raise forms.ValidationError(u'O conteúdo da página deve ter um texto em destaque!\n Este texto deve ser uma parte importante do conteúdo para ser reforçada com o aluno!')


        return self.cleaned_data['content_page']


class ExerciseForm(ModelForm):

    class Meta:

        model = Exercise

    answer1 = forms.CharField(widget=forms.TextInput(attrs={'style': "width:890px;"}))
    answer2 = forms.CharField(widget=forms.TextInput(attrs={'style': "width:890px;"}))
    answer3 = forms.CharField(widget=forms.TextInput(attrs={'style': "width:890px;"}))
    answer4 = forms.CharField(widget=forms.TextInput(attrs={'style': "width:890px;"}))



