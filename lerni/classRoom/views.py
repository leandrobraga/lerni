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
from lerni.domain.models import Topic

import time
from datetime import timedelta
from datetime import datetime


@login_required
def index(request):

    student = Student.objects.get(user=request.user)
    request.session['student'] = student
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

    request.session['pratical_token'] = 0



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

        request.session['theoretical_initial_time'] = time.time()

    #Inicia contagem de tempo do exercio teórico e finaliza o prático
    if page == 6:

        request.session['theoretical_final_time'] = time.time()

        if request.session['pratical_token'] == 0:
            request.session['pratical_initial_time'] = time.time()
            request.session['pratical_token'] = 1

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

    pratical_initial_time = request.session['pratical_initial_time']
    pratical_total = time.time() - pratical_initial_time
    pratical_time_spent = datetime(1, 1, 1) + timedelta(seconds=(pratical_total))

    theoretical_initial_time = request.session['theoretical_initial_time']
    theoretical_total = time.time() - theoretical_initial_time
    theoretical_time_spent = datetime(1, 1, 1) + timedelta(seconds=(theoretical_total))

    student = request.session['student']

    answers = request.session['answers']

    hits_theoretical, hits_pratical = check_answers(answers)

    complexity_theoretical, complexity_pratical = get_complexity(answers)

    time_theoretical, time_pratical = get_time(answers)

    tutor = Tutor()

    tutor.theoretical_fuzzification(theoretical_time_spent.minute, time_theoretical, hits_theoretical, complexity_theoretical)
    grade_theoretical_fuzzification = tutor.inferencia()
    grade_theoretical_defuzzification = tutor.defuzificacao()

    tutor.pratical_fuzzification(pratical_time_spent.minute, time_pratical, hits_pratical, complexity_pratical)
    grade_pratical_fuzzification = tutor.inferencia()
    grade_pratical_defuzzification = tutor.defuzificacao()

    tutor.fuziffication_final(grade_theoretical_defuzzification, grade_pratical_defuzzification)
    grade_final_fuzzification = tutor.inferencia_final()
    grade_final_defuzzification = tutor.defuzificacao_final()

    grade_theoretical_traditional, grade_pratical_traditional, grade_final = get_grades(hits_theoretical, hits_pratical)

    topic = student.study_context.current_topic

    if grade_final >= 6:

        next_topic = Topic.objects.filter(position=topic.position + 1).get()
        first_page = Page.objects.filter(topic=next_topic).filter(number=1).get()

        student.study_context.current_topic = next_topic
        student.study_context.current_page = first_page
        student.study_context.save()

    else:

        first_page = Page.objects.filter(topic=topic).filter(number=1).get()
        student.study_context.current_page = first_page

    student.grade.topic = topic
    student.grade.grade_teoretical = grade_theoretical_traditional
    student.grade.grade_pratical = grade_pratical_traditional
    student.grade.grade_final = grade_final
    student.grade.grade_fuzzy_teoretical = grade_theoretical_defuzzification
    student.grade.grade_fuzzy_pratical = grade_pratical_defuzzification
    student.grade.grade_fuzzy_final = grade_final_defuzzification

    student.grade.save()

    student.level_learning = get_level(grade_final_fuzzification)
    student.level_learning_theoretical = get_level(grade_theoretical_fuzzification)
    student.level_learning_pratical = get_level(grade_pratical_fuzzification)

    student.save()

    return render(request, "classRoom/final_exercise.html", locals())


def detail_answers(answers):

    correct_answers = []

    for answer in answers:
        exercise = Exercise.objects.get(pk=answer[0])

        if int(exercise.correctAnswer) == int(answer[1]):

            correct_answers.append(int(answer[1]), exercise.correctAnswer, True)

        else:

            correct_answers.append(int(answer[1]), exercise.correctAnswer, False)

    return correct_answers


def check_answers(answers):

    #correct_answers = []

    hits_theoretical = 0
    hits_pratical = 0

    for x, answer in enumerate(answers):
        exercise = Exercise.objects.get(pk=answer[0])

        if int(exercise.correctAnswer) == int(answer[1]):
            if x + 1 <= 5:

                hits_theoretical += 1

            else:
                hits_pratical += 1

    return hits_theoretical, hits_pratical


def get_complexity(answers):

    complexity_theoretical = 0
    complexity_pratical = 0

    for x, answer in enumerate(answers):

        exercise = Exercise.objects.get(pk=answer[0])

        if int(x) + 1 <= 5:

            complexity_theoretical += exercise.level

        else:

            complexity_pratical += exercise.level

    return (complexity_theoretical) / 5, (complexity_pratical) / 3


def get_time(answers):

    time_theoretical = 0
    time_pratical = 0

    for x, answer in enumerate(answers):
        exercise = Exercise.objects.get(pk=answer[0])

        if int(x) + 1 <= 5:

            time_theoretical += exercise.time

        else:

            time_pratical += exercise.time

    return time_theoretical, time_pratical


def get_grades(theoretical, pratical):

    return round((theoretical * 10 / 5), 2), round((pratical * 10 / 3), 2), round(((theoretical + pratical) * 10 / 8))


def get_level(grade_fuzification):

    higher = grade_fuzification.items()[0][1]
    level = grade_fuzification.items()[0][0]

    for term, value in grade_fuzification:

        if value > higher:
            higher = value
            level = term

    return level




