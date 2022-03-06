from datetime import datetime, timedelta

from django.core.mail import send_mail
from task_manager.celery import app

from .models import Task, TaskReminder


@app.task
def send_email_reminder():
    print('Running every minute ...')
    task_reminders=TaskReminder.objects.filter(last_sent__lte = datetime.now().astimezone() - timedelta(hours=24))
    for task_reminder in task_reminders:
        print(task_reminder.last_sent)
        task_reminder.last_sent = datetime.now().astimezone()
        task_reminder.save()
        print(task_reminder.last_sent)
        user = task_reminder.user
        qs = Task.objects.filter(user=user, deleted=False)
        pending = qs.filter(status='PENDING')
        completed = qs.filter(status='COMPLETED')
        in_progress = qs.filter(status='IN_PROGRESS')
        cancelled = qs.filter(status='CANCELLED')
        email_content = f"You have {pending.count()} pending tasks, {completed.count()} completed tasks,\n {in_progress.count()} tasks in progress and {cancelled.count()} tasks cancelled"
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
