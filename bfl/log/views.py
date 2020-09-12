from django.shortcuts import render
from django.http import HttpResponse

def landing(request):
    return HttpResponse('<h1>Landing</h1>')
