#! coding: utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as authlogin
from django.contrib.auth import logout as authlogout
from lerni.core.models import Teacher
from lerni.core.models import Student
from django.contrib.auth.decorators import login_required


def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        userLoged = authenticate(username=username, password=password)

        if userLoged is not None:

            if userLoged.is_active:

                authlogin(request, userLoged)

                if Teacher.objects.filter(user=userLoged):

                    return redirect('/teacher/')

                if Student.objects.filter(user=userLoged):
                    return redirect("/student/")

                return redirect('/administrator/')

            else:
                return render(request, 'core/index.html', {'error_message': 'Seu usuário está desativado!'})
        else:
            return render(request, 'core/index.html', {'error_message': 'Login ou Senha inválidos!'})
    else:
        return redirect('core_index')


@login_required
def logout(request):

    authlogout(request)
    return redirect('/')


