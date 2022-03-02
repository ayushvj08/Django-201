from django.forms import ModelForm
from django.shortcuts import redirect
from .models  import Task , TaskReminder
from django.views.generic.edit import CreateView, UpdateView, DeleteView, ModelFormMixin
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class AuthorisedTaskManager(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(deleted=False, user=self.request.user)

class TaskReminderUpdateView(UpdateView):
    model = TaskReminder
    fields = ['reminder_time']
    template_name = "task/reminder_form.html"
    success_url  = "/task/list/"

class TaskReminderCreateView(AuthorisedTaskManager, CreateView):
    model = TaskReminder
    fields = ['reminder_time']
    template_name = "task/reminder_form.html"
    success_url  = "/task/list/"
    def form_valid(self, form):
        print(form.cleaned_data.get('reminder_time'))
        self.object = form.save()
        self.object.user=self.request.user
        return super().form_valid(form)

class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "priority", "completed")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'p-label rounded-lg'
        self.fields['title'].widget.attrs['autofocus'] = True
        self.fields['description'].widget.attrs['class'] = 'p-label rounded-lg'
        self.fields['description'].widget.attrs['rows'] = '8'
        self.fields['priority'].widget.attrs['class'] = 'p-label rounded-lg'
        self.fields['completed'].widget.attrs['class'] = 'rounded'
        
class TaskFormMixin(ModelFormMixin):
    def form_valid(self, form):
        if 'priority' in form.changed_data:
            priority = form.cleaned_data["priority"]
            tasks = Task.objects.filter(completed=False, deleted=False)
            objs = []
            same_priority_task = tasks.filter(priority=priority)
            while same_priority_task.exists():
                task = same_priority_task[0]
                task.priority = priority + 1
                objs.append(task)
                priority +=1
                same_priority_task = tasks.filter(priority=priority)

            Task.objects.bulk_update(objs, ['priority'])

        self.object = form.save()
        self.object.user  = self.request.user
        self.object.save()
        return redirect(self.get_success_url())

class TaskCreateView(TaskFormMixin, AuthorisedTaskManager, CreateView):
    form_class = TaskCreateForm
    template_name = "task/task_form.html"
    success_url  = "/task/list/"

class TaskUpdateView(TaskFormMixin, AuthorisedTaskManager, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task/task_form.html"
    success_url  = "/task/list/"

class DeleteTaskView(AuthorisedTaskManager, DeleteView):
    model = Task
    success_url  = "/task/list/"

class TaskListView(AuthorisedTaskManager, ListView):
    queryset = Task.objects.filter(deleted=False)
    template_name = "task/list.html"
    context_object_name = "tasks"
    paginate_by = 5
    
    def get_queryset(self):
        tasks = Task.objects.filter(deleted=False, user=self.request.user).order_by('priority')
        if self.request.path == "/task/list/completed/":
            tasks = tasks.filter(completed=True)
        elif self.request.path == "/task/list/pending/":
            tasks = tasks.filter(completed=False)
        return tasks
