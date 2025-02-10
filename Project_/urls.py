from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from Project_ import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('navbar/', views.navbar, name='navbar'),
    path('create/', views.create, name='create'),
    path('get/', views.success, name='get'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('get_id/<int:pk>/', views.get_id, name='getId')
]