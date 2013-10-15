# coding: utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from lerni.core.models import Student
from lerni.tutor.models import Tutor
from lerni.domain.models import Exercise
from lerni.domain.models import Page

import json
import time


@login_required
def index(request):

    student = Student.objects.get(user=request.user)
    return render(request, "classRoom/index.html", locals())


@login_required
def get_page(request, student_id):

    student = get_object_or_404(Student, pk=student_id)
    current_topic = current_topic = student.study_context.current_topic
    tutor = Tutor()
    pages_list = Page.objects.filter(topic=current_topic).all()
    paginator = Paginator(pages_list, 1)

    #  Certifica que a pagina será um inteiro.verifica de qual input a pagina veio
    if request.method == 'POST':

        if "next" in request.POST:

            try:

                page = int(request.POST['page_next'])

            except:

                page = 1

            tutor.next_page(student)

        elif 'previous' in request.POST:

            try:

                page = int(request.POST['page_previous'])

            except:

                page = 1

            tutor.previous_page(student)

        #Existe um terceiro submit que é qdo inicia a aula neste não tem next_page ou previous_page.
        else:

            try:
                request.POST['first']
                page = int(request.POST['first'])

            except:

                page = 1

    else:

        return redirect('/classRoom/')

    # Se o page request (9999) está fora da lista, mostre a última página.
    print page
    try:
        content_page = paginator.page(page)

        topic_page = tutor.get_formated_page(student)

    except (EmptyPage, InvalidPage):

        #exercise1 = paginator.page(paginator.num_pages)
        #exercise = question_list[page - 1]
        return redirect('/classRoom/exercise/')

    return render(request, "classRoom/content.html", locals())


@login_required
def exercise(request):

    student = Student.objects.get(user=request.user)
    current_topic = student.study_context.current_topic

    theoretical_list = Exercise.objects.filter(kind=1).filter(topic=current_topic).order_by('?').all()[:5]
    pratical_list = Exercise.objects.filter(kind=2).filter(topic=current_topic).order_by('?').all()[:3]

    request.session['question_list'] = list(theoretical_list) + list(pratical_list)
    request.session['answers'] = (["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""])

    request.session['time']

    #request.session['total_time_theoretical'] = 0
    #request.session['questions_theoretical'] = questions_theoretical
    #request.session['number_question_theoretical'] = 0

    #questions_pratical = Exercise.objects.filter(kind=2).filter(topic=current_topic).order_by('?').all()[:3]

    #request.session['total_time_pratical'] = 0
    #request.session['questions_pratical'] = questions_pratical
    #request.session['number_question_pratical'] = 0

    return render(request, "classRoom/exercise_index.html", locals())


@login_required
def get_exercise(request):

    question_list = request.session['question_list']
    paginator = Paginator(question_list, 1)

    #  Certifica que a pagina será um inteiro.verifica de qual input a pagina veio
    if request.method == 'POST':

        if "next" in request.POST:

            try:

                page = int(request.POST['page_next'])

            except:

                page = 1

            # Verifica se tem uma reposta no POST se não tiver não avança a págna e mostra um erro
            if not "answer" in request.POST:
                if page > 1:
                    page -= 1

                noSelected = 1

            else:

                answers = request.session['answers']
                answers[page - 2][0]=request.POST['exercise_id']
                answers[page - 2][1]=request.POST['answer']
                request.session['answers'] = answers
                if page <= paginator.num_pages:
                    checked = answers[page-1][1]

        else:

            try:

                page = int(request.POST['page_previous'])

            except:

                page = 1

            answers = request.session['answers']
            checked = answers[page-1][1]

    else:
        page = 1


    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        exercise1 = paginator.page(page)
        exercise = question_list[page - 1]

    except (EmptyPage, InvalidPage):

        #exercise1 = paginator.page(paginator.num_pages)
        #exercise = question_list[page - 1]
        return redirect('/classRoom/endExercise/')

    return render(request, "classRoom/exercise.html", locals())


@login_required
def end_exercise(request):

    tutor = Tutor()
    return render(request, "classRoom/final_exercise.html", locals())