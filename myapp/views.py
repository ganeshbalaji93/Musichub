from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from .forms import DisplayForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'myapp/home.html')


def custom_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/myapp/home')

        else:
            error = True
            return render(request, 'myapp/login.html', {'error': error})
    else:
        return render(request, 'myapp/login.html')


def registration(request):
    if request.method == 'POST':
        form = DisplayForm(request.POST)
        if form.is_valid():
            userobj = form.cleaned_data
            username = userobj['username']
            email = userobj['email']
            password = userobj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/mysongs/createnewalbum')
            else:
                error = True
                return render(request, 'myapp/register.html', {'error': error})

    else:
        form = DisplayForm()
    return render(request, 'myapp/register.html', {'form': form})

@login_required
def custom_logout(request):
    logout(request)
    return render(request, 'myapp/logout.html')








