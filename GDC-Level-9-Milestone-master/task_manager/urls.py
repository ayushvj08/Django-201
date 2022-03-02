from django.contrib import admin
from django.urls import include, path

from .views import UserLoginView, UserCreateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("task/", include('tasks.urls')),
    path('user/signup/', UserCreateView.as_view()),
    path('user/login/', UserLoginView.as_view()),
    path('', UserLoginView.as_view()),
    path('user/logout/', LogoutView.as_view())
]