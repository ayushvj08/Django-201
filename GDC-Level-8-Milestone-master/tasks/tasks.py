from task_manager.celery import app
from datetime import datetime, timedelta
from .models import TaskReminder, User, Task

from django.core.mail import send_mail

@app.task
def send_email_reminder():
    print('Polling for Email Processing every 60 seconds ...')
    task_reminders=TaskReminder.objects.filter(reminder_time__range=[datetime.now(), datetime.now()+timedelta(seconds=60)])
    for task_reminder in task_reminders:
        user = task_reminder.user
        qs = Task.objects.filter(user=user, deleted=False)
        pending = qs.filter(status='PENDING')
        completed = qs.filter(status='COMPLETED')
        in_progress = qs.filter(status='IN_PROGRESS')
        cancelled = qs.filter(status='CANCELLED')
        email_content = f"""You have {pending.count()} pending tasks, {completed.count()} completed tasks,\n {in_progress.count()} tasks in progress and {cancelled.count()} tasks cancelled"""

        send_mail(
        'Mail from django task manager',
        email_content,
        'django@service.com',
        ['test@gmail.com']  ## user.email
        )
        
        print(f'completed Processing user_id {user.id} ')


app.conf.beat_schedule = {
    'key':{
        'task':'tasks.tasks.send_email_reminder',
        'schedule': timedelta(seconds=60),
    }
}
