from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path('master', include('master.urls.py')),

]