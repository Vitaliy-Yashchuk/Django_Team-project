from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from Project_ import views 

urlpatterns = [
    path('navbar/', views.navbar, name='navbar'),
    path('create/', views.create, name='create'),
    path('get/', views.get_protocol, name='get'),
]