from django.http import HttpResponse # type: ignore
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.urls import reverse # type: ignore
import logging
from Project_.models import DTP
from .forms import DTPForm 
from .models import DTP

def home(request):
    print("Функція home викликається!")
    dtp = DTP.objects.all()
    return render(request, 'index.html', {'dtp': dtp})


def navbar(request):
     return render(request, 'NavBar.html',)

# def create(request):
#     return render(request, 'create.html',)


def get_protocol(request):
    return render(request, 'success.html',)
    
def create(request):
    if request.method == "POST":
        form = DTPForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправлення на головну сторінку після збереження
    else:
        form = DTPForm()

    return render(request, 'create.html', {'form': form})