from task_manager.celery import app
from datetime import datetime, timedelta
from .models import TaskReminder, Task

from django.core.mail import send_mail

@app.task
def send_email_reminder():
    print('Running every 30 minutes ...')
    task_reminders=TaskReminder.objects.filter(reminder_time__range=[datetime.now() - timedelta(hours=8), datetime.now()])
    for task_reminder in task_reminders:
        time = datetime.now().date() - task_reminder.last_sent.date()
        if time >= timedelta(hours=24):
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
            task_reminder.last_sent = datetime.now()
            task_reminder.save()
            print(f'completed Processing user_id {user.id} ')


app.conf.beat_schedule = {
    'key':{
        'task':'tasks.tasks.send_email_reminder',
        'schedule': timedelta(minutes=30),
    }
}
