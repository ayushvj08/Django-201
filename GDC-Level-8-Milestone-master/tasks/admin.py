from django.contrib import admin

# Register your models here.

from tasks.models import Task, TaskHistory, TaskReminder

admin.sites.site.register(Task)
admin.sites.site.register(TaskHistory)
admin.sites.site.register(TaskReminder)