from django.contrib import admin
from django.urls import path, include
from takeexam import views

urlpatterns = [
    path('exampage', views.exampage, name='exampage'),
    path('completion', views.completion, name='completion'),
    # path('', include('loginPage.urls')),
]
