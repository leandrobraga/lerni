#! coding: utf-8

import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from lerni.core.forms import UserAddForm
from lerni.core.forms import UserUpdateForm
from lerni.core.models import Teacher
from lerni.core.models import Student
from lerni.core.models import StudyContext
from lerni.core.models import Grades
from lerni.domain.models import Topic
from lerni.domain.models import Page

def index(request):

    return render(request, 'core/index.html')


@login_required
def administrator(request):

    request.session['menu_type'] = 'administrator'
    return render(request, 'core/administrator.html', locals())


@login_required
def teacher(request):

    request.session['menu_type'] = 'teacher'
    return render(request, 'core/teacher.html', locals())


@login_required
def choose_user(request):

    return render(request, "core/chooseUser.html", locals())


@login_required
def manager_teacher(request):

    teachers = Teacher.objects.all()

    return render(request, "core/managerTeacher.html", locals())


@login_required
def add_teacher(request):

    if request.method == 'POST':
        return create_teacher(request)
    else:
        return new_teacher(request)


@login_required
def create_teacher(request):

    form = UserAddForm(request.POST)

    if not form.is_valid():

        return render(request, "core/addTeacher.html", locals())

    user = form.save()
    teacher = Teacher(user=user)
    teacher.save()

    form = UserAddForm()
    addTeacherSucess = 1

    return render(request, "core/addTeacher.html", locals())


@login_required
def new_teacher(request):

    form = UserAddForm()
    return render(request, "core/addTeacher.html", locals())


@login_required
def detail_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)

    teacherJson = {
        'name': teacher.user.get_full_name(), 'email': teacher.user.email, 'id': teacher.user.id, 'user': teacher.user.username,
        'date_joined': teacher.user.date_joined.strftime("%d/%m/%Y"),
        'last_login': teacher.user.last_login.strftime("%d/%m/%Y - %H:%M")
    }

    return HttpResponse(json.dumps(teacherJson), mimetype="text/json")


@login_required
def change_teacher(request, teacher_id):

    if request.method == "POST":

        return update_teacher(request, teacher_id)

    else:

        return show_update_form_teacher(request, teacher_id)


@login_required
def update_teacher(request, teacher_id):

    teacher = get_object_or_404(Teacher, pk=teacher_id)

    form = UserUpdateForm(request.POST, instance=teacher.user)

    if not form.is_valid():

        return render(request, "core/changeTeacher.html", locals())

    teacher.user.first_name = request.POST['first_name']
    teacher.user.last_name = request.POST['last_name']
    teacher.user.email = request.POST['email']
    teacher.user.username = request.POST['username']
    teacher.user.save()
    teacher.save()

    teacherChangeSucess = 1

    return render(request, "core/changeTeacher.html", locals())

@login_required
def show_update_form_teacher(request, teacher_id):

    teacher = get_object_or_404(Teacher, pk=teacher_id)
    form = UserUpdateForm(instance=teacher.user)
    return render(request, "core/changeTeacher.html", locals())


@login_required
def delete_teacher(request, teacher_id):

    teacher = get_object_or_404(Teacher, pk=teacher_id)
    user = get_object_or_404(User, pk=teacher.user.id)

    user.delete()
    teacher.delete()

    deleteTeacherSucess = 1

    return render(request, "core/deleteTeacherSucess.html", locals())


@login_required
def manager_student(request):

    students = Student.objects.all()

    return render(request, "core/managerStudent.html", locals())


@login_required
def add_student(request):

    if request.method == 'POST':

        return create_student(request)
    else:

        return new_student(request)


@login_required
def create_student(request):

    form = UserAddForm(request.POST)

    if not form.is_valid():

        return render(request, "core/addStudent.html", locals())

    user = form.save()
    student = Student(user=user)
    student.level_learning = 'assistant'
    student.level_learning_theoretical = 'assistant'
    student.level_learning_pratical = 'assistant'

    topicFirst = Topic.objects.filter(position=1).get()
    pageFirst = Page.objects.filter(topic=topicFirst).filter(number=1).get()
    studyContext = StudyContext(current_topic=topicFirst, current_page=pageFirst, finished=0)
    studyContext.save()
    student.study_context = studyContext

    student.save()

    #student.grades_set.create(topic=topicFirst, grade_teoretical=0, grade_pratical=0, grade_final=0,
    #grade_fuzzy_teoretical=0, grade_fuzzy_pratical=0, grade_fuzzy_final=0)

    form = UserAddForm()
    addStudentSucess = 1

    return render(request, "core/addStudent.html", locals())


@login_required
def new_student(request):

    form = UserAddForm()
    return render(request, "core/addStudent.html", locals())


@login_required
def detail_student(request, student_id):

    student = get_object_or_404(Student, pk=student_id)

    studentJson = {
        'name': student.user.get_full_name(), 'email': student.user.email, 'id': student.user.id, 'user': student.user.username,
        'date_joined': student.user.date_joined.strftime("%d/%m/%Y"), 'last_login': student.user.last_login.strftime("%d/%m/%Y - %H:%M"),
    }

    return HttpResponse(json.dumps(studentJson), mimetype="text/json")


@login_required
def change_student(request, student_id):

    if request.method == "POST":

        return update_student(request, student_id)

    else:

        return show_update_form_student(request, student_id)


@login_required
def update_student(request, student_id):

    student = get_object_or_404(Student, pk=student_id)

    form = UserUpdateForm(request.POST, instance=student.user)

    if not form.is_valid():

        return render(request, "core/changeTeacher.html", locals())

    student.user.first_name = request.POST['first_name']
    student.user.last_name = request.POST['last_name']
    student.user.email = request.POST['email']
    student.user.username = request.POST['username']
    student.user.save()
    student.save()

    studentChangeSucess = 1

    return render(request, "core/changeStudent.html", locals())


@login_required
def show_update_form_student(request, student_id):

    student = get_object_or_404(Student, pk=student_id)
    form = UserUpdateForm(instance=student.user)

    return render(request, "core/changeStudent.html", locals())

@login_required
def delete_student(request, student_id):

    student = get_object_or_404(Student, pk=student_id)
    user = get_object_or_404(User, pk=student.user.id)

    deleteStudentSucess = 1

    user.delete()
    student.delete()

    return render(request, "core/deleteStudentSucess.html", locals())


@login_required
def student(request):

    student = Student.objects.filter(user=request.user).get()
    request.session['menu_type'] = 'student'
    number_of_topics = Topic.objects.all().count()
    completed_topics = Grades.objects.filter(finished=1).all().count()

    percentage_of_completed_topics = str((completed_topics*100)/number_of_topics)+'%'

    return render(request, "core/student.html", locals())
