from .views import ProjectsListView, ProjectDetailView
from django.urls import path

urlpatterns = [
    path('projects/', ProjectsListView.as_view()),
    path('projects/<int:pk>', ProjectDetailView.as_view()),
]
