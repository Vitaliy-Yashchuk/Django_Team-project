from django.http import HttpResponse # type: ignore
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.urls import reverse # type: ignore
import logging
from Project_.models import DTP

def home(request):
    dtp = DTP.objects.all()
    return render(request, 'home.html', {'dtp': dtp})

def navbar(request):
     return render(request, 'NavBar.html',)