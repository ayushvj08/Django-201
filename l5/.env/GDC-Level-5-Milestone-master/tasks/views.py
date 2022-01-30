from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from tasks.models import Task
# Create your views here.

def tasks_view(request):
    tasks = Task.objects.filter(deleted=False, completed=False)
    # return HttpResponse("<h1>Hi There</h1>")
    return render(request, "task.html", {"tasks": tasks})

def add_task_view(request):
    task_value = request.GET.get("task")
    # tasks.append(task_value)
    task_obj = Task(title=task_value)
    task_obj.save()
    return HttpResponseRedirect("/tasks")

def delete_task_view(request, index ):
    # del tasks[index - 1]
    Task.objects.filter(id=index).update(deleted=True)
    return HttpResponseRedirect("/tasks")

def complete_task_view(request, id):
    # completed_task = tasks.pop(id - 1)
    completed_task = Task.objects.filter(id=id).update(completed=True)
    # completed.append(completed_task)
    return HttpResponseRedirect("/tasks")

def all_tasks_view(request):
    tasks = Task.objects.filter(deleted=False, completed=False)
    completed = Task.objects.filter(completed=True, deleted=False)
    return render(request, "all_tasks.html", {"tasks": tasks, "completed": completed})

def completed_tasks_view(request):
    completed = Task.objects.filter(completed=True, deleted=False)
    return render(request, "completed_tasks.html", {"completed": completed})
# Add your Views Here
