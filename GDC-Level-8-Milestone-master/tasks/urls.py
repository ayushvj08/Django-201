from django.urls import path
from . import views
from . import api_views

from rest_framework import routers
router = routers.SimpleRouter()
router.register('api/list', api_views.TaskViewSet)
router.register('api/history', api_views.HistoryViewSet)
from . import tasks

urlpatterns = [
    path('new/', views.TaskCreateView.as_view()),
    path('<pk>/update/', views.TaskUpdateView.as_view()),
    path('<pk>/delete/', views.DeleteTaskView.as_view()),
    path('list/', views.TaskListView.as_view()),
    path('list/pending/', views.TaskListView.as_view()),
    path('list/completed/', views.TaskListView.as_view()),
    # path('email/', tasks.mail),
    path('set_mail_time/', views.TaskReminderCreateView.as_view()),
    path('<pk>/edit_mail_time/', views.TaskReminderUpdateView.as_view()),
] + router.urls