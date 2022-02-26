from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.TaskCreateView.as_view()),
    path('<pk>/update/', views.TaskUpdateView.as_view()),
    path('<pk>/delete/', views.DeleteTaskView.as_view()),
    path('list/', views.TaskListView.as_view()),
    path('list/pending/', views.TaskListView.as_view()),
    path('list/completed/', views.TaskListView.as_view())
]