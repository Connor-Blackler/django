"""Urls used with the project app"""
from django.urls import path
from .views import project, projects


urlpatterns = [
    path('', projects, name="Projects"),
    path('projects/<str:pk>/', project, name="project"),
]
