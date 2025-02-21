from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from Project_ import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('project/', include('Project_.urls')),
    
]
