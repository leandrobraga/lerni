# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from lerni.domain.models import Topic
from lerni.domain.models import Exercise
from lerni.domain.models import Page

from lerni.domain.forms import TopicForm
from lerni.domain.forms import PageForm
from lerni.domain.forms import ExerciseForm

import json


def index(request):

    return render(request, "domain/index.html", locals())


@login_required
def topic(request):

    topics = Topic.objects.all().order_by('position')

    return render(request, 'domain/topic.html', locals())


@login_required
def add_topic(request):

    if request.method == 'POST':

        return create_topic(request)

    else:

        return new_topic(request)


@login_required
def create_topic(request):
    form = TopicForm(request.POST)

    if not form.is_valid():

        return render(request, 'domain/addTopic.html', locals())

    form.save()

    form = TopicForm()

    addTopicSucess = 1

    return render(request, 'domain/addTopic.html', locals())


@login_required
def new_topic(request):

    form = TopicForm()

    return render(request, "domain/addTopic.html", locals())


@login_required
def change_topic(request, topic_id):

    if request.method == "POST":

        return update_topic(request, topic_id)

    else:

        return show_update_form_topic(request, topic_id)


@login_required
def update_topic(request, topic_id):

    topic = get_object_or_404(Topic, pk=topic_id)

    form = TopicForm(request.POST, instance=topic)

    if not form.is_valid():

        return render(request, "domain/changeTopic.html", locals())

    form.save()
    form = TopicForm()

    topicChangeSucess = 1

    return render(request, "domain/changeTopic.html", locals())


@login_required
def show_update_form_topic(request, topic_id):

    topic = get_object_or_404(Topic, pk=topic_id)
    form = TopicForm(instance=topic)

    return render(request, "domain/changeTopic.html", locals())


@login_required
def delete_topic(request, topic_id):

    topic = get_object_or_404(Topic, pk=topic_id)

    pages = Page.objects.filter(topic=topic).all()

    topics = Topic.objects.filter(position__gt=topic.position).all()



    if pages:
        for page in pages:
            page.delete

    topic.delete()

    if topics:
        for topic1 in topics:
            topic1.position -= 1
            topic1.save()

    deleteTopicSucess = 1

    return render(request, "domain/deleteTopicSucess.html", locals())

@login_required
def page(request, topic_id):

    topic = get_object_or_404(Topic, pk=topic_id)
    pages = Page.objects.order_by('number').filter(topic=topic).all()

    return render(request, "domain/page.html", locals())


@login_required
def add_page(request, topic_id):

    if request.method == 'POST':
        return create_page(request, topic_id)
    else:
        return new_page(request, topic_id)


@login_required
def new_page(request, topic_id):

    topic = get_object_or_404(Topic, pk=topic_id)
    #pages = Page.objects.filter(topic=topic).all()

    form = PageForm(initial={'number':(topic.get_total_pages()+1)})
    return render(request, "domain/addPage.html", locals())


@login_required
def create_page(request, topic_id):

    form = PageForm(request.POST)
    topic = get_object_or_404(Topic, pk=topic_id)

    if not form.is_valid():

        return render(request, "domain/addPage.html", locals())

    page = Page(content_page=form.cleaned_data['content_page'], number=form.cleaned_data['number'], topic=topic)
    page.save()

    form = PageForm(initial={'number':(topic.get_total_pages()+1)})

    addPageSucess = 1

    return render(request, "domain/addPage.html", locals())


@login_required
def delete_page(request, page_id):

    page = get_object_or_404(Page, pk=page_id)

    pages = Page.objects.filter(number__gt=page.number).all()

    page.delete()

    if pages:
        for page in pages:
            page.number -= 1
            page.save()

    topic = page.topic

    deletePageSucess = 1

    return render(request, "domain/deletePageSucess.html", locals())


@login_required
def change_page(request, page_id):

    if request.method == "POST":

        return update_page(request, page_id)

    else:

        return show_update_form_page(request, page_id)


@login_required
def show_update_form_page(request, page_id):

    page = get_object_or_404(Page, pk=page_id)
    form = PageForm(instance=page)

    return render(request, "domain/changePage.html", locals())


@login_required
def update_page(request, page_id):

    page = get_object_or_404(Page, pk=page_id)
    form = PageForm(request.POST, instance=page)

    if not form.is_valid():

        return render(request, "domain/changePage.html", locals())

    page.conte_page = form.cleaned_data['content_page']
    page.number = form.cleaned_data['number']

    page.save()
    topic = page.topic
    pageChangeSucess = 1

    return render(request, "domain/changePage.html", locals())


@login_required
def exercise(request):

    exercises = Exercise.objects.all()

    return render(request, "domain/exercise.html", locals())


@login_required
def add_exercise(request):

    if request.method == 'POST':

        return create_exercise(request)
    else:

        return new_exercise(request)

@login_required
def new_exercise(request):

    form = ExerciseForm()
    return render(request, "domain/addExercise.html", locals())

@login_required
def create_exercise(request):

    form = ExerciseForm(request.POST)

    if not form.is_valid():

        return render(request, "domain/addExercise.html", locals())

    form.save()

    form = ExerciseForm()

    addExerciseSucess = 1

    return render(request, "domain/addExercise.html", locals())

@login_required
def detail_exercise(request, exercise_id):

    exercise = get_object_or_404(Exercise, pk=exercise_id)

    exerciseJson = {
        'question': exercise.question, 'answer1': exercise.answer1,
        'answer2': exercise.answer2, 'answer3': exercise.answer3,
        'answer4': exercise.answer4, 'correctAnswer': exercise.correctAnswer,
        'topic': exercise.topic.title, 'level': exercise.level,
        'time': exercise.time, 'kind': exercise.kind,
    }

    return HttpResponse(json.dumps(exerciseJson), mimetype="text/json")


@login_required
def change_exercise(request, exercise_id):

    if request.method == 'POST':

        return update_exercise(request, exercise_id)

    else:

        return show_update_form_exercise(request, exercise_id)


@login_required
def show_update_form_exercise(request, page_id):

    exercise = get_object_or_404(Exercise, pk=page_id)
    form = ExerciseForm(instance=exercise)

    return render(request, "domain/changeExercise.html", locals())


@login_required
def update_exercise(request, exercise_id):

    exercise = get_object_or_404(Exercise, pk=exercise_id)
    form = ExerciseForm(request.POST, instance=exercise)

    if not form.is_valid():

        return render(request, "domain/changeExercise.html", locals())

    form.save()
    form = ExerciseForm()

    exerciseChangeSucess = 1

    return render(request, "domain/changeExercise.html", locals())

@login_required
def delete_exercise(request, exercise_id):

    exercise = get_object_or_404(Exercise, pk=exercise_id)

    exercise.delete()

    deleteExerciseSucess = 1

    return render(request, "domain/deleteExerciseSucess.html", locals())

