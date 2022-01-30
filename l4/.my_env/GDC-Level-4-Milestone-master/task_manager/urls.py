from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

tasks = []
completed = []

def tasks_view(request):
    # return HttpResponse("<h1>Hi There</h1>")
    return render(request, "task.html", {"tasks": tasks})

def add_task_view(request):
    task_value = request.GET.get("task")
    tasks.append(task_value)
    return HttpResponseRedirect("/tasks")

def delete_task_view(request, index ):
    del tasks[index - 1]
    return HttpResponseRedirect("/tasks")

def complete_task_view(request, id):
    completed_task = tasks.pop(id - 1)
    completed.append(completed_task)
    return HttpResponseRedirect("/tasks")

def all_tasks_view(request):
    return render(request, "all_tasks.html", {"tasks": tasks, "completed": completed})

def completed_tasks_view(request):
    return render(request, "completed_tasks.html", {"completed": completed})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',tasks_view),
    path('tasks/',tasks_view),
    path('add-task/',add_task_view ),
    path('delete-task/<int:index>/', delete_task_view),
    path('complete_task/<int:id>/', complete_task_view),
    path('all_tasks/',all_tasks_view),
    path('completed_tasks/', completed_tasks_view)
]
