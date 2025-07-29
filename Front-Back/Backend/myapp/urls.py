from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views
from .views import myapp, Main

urlpatterns = [
   
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('myapp/', myapp, name='myapp'),
    path('aichat/', Main, name='chat_view'),
]
