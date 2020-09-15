from django.shortcuts import render
from django.http import HttpResponse

def landing(request):
    return render(request, 'log/pages/landing.html')

def caa(request):
    context = {
        'title': 'Signup'
    }
    return render(request, 'log/pages/caa.html', context)

def login(request):
    context = {
        'title': 'Login'
    }
    return render(request, 'log/pages/login.html', context)
