from django.contrib import admin
from django.urls import path, include
from . import views as iftp_views

urlpatterns = [
    path('gmail/new/', iftp_views.get_new_gmail, name='get_new_gmail'),
]