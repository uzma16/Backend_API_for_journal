from .service import send_notification
from reminders.models import Reminder
from accounts.models import User
from mindfulness.celery import app
import random
from prompts.views import PromptDetail
import datetime
import pytz

def truncate_text(text, length):
    if len(text) > length:
        return text[:length] + "..."
    return text


@app.task(name='reminder_cron_job')
def reminder_cron_job():
    cur_time = datetime.datetime.now().replace(microsecond=0)
    reminders = Reminder.objects.filter(is_active=True, time__exact=cur_time)
    for reminder in reminders:
        if len(reminder.label) == 0:
            labels = [
                'Journal Reminder',
                'Reminder to unleash your thoughts',
                'Reminder to Let it go!'
            ]
            title = random.choice(labels)
            body = "Unlock your thoughts and journal your journey. It's time for your scheduled journaling."
        else:
            title = reminder.label
            body = "Reflect and Reconnect: A gentle reminder to get back to your journal."
        user = User.objects.get(username=reminder.user)
        user_token = user.fcm_token[-1]
        send_notification(user_token, title, body, notification_type='Reminder Notification')
        if reminder.repeat == 'Once':
            reminder.is_active = False
            reminder.save()
        elif reminder.repeat == 'Everyday':
            reminder.time += datetime.timedelta(days=1)
            reminder.save()
        elif reminder.repeat == 'Custom':
            day_index = cur_time.weekday()
            if reminder.days_of_week[day_index]:
                reminder.time += datetime.timedelta(days=1)
                reminder.save()
    return "reminder notification sent"


@app.task(name='last_login')
def last_login():
    cur_time = datetime.datetime.now().date()
    users = User.objects.all()
    for user in users:
        if user.is_admin:
            pass
        else:
            user_token = user.fcm_token[-1]
            time_difference = user.last_login.date() - cur_time
            if time_difference.days == 5:
                send_notification(user_token, title="It's been a while", body="Rediscover the joy of "
                                                                              "writing: open your journal app and let "
                                                                              "your thoughts flow freely once again",
                                  notification_type="Last Login Notification")
    return "last login sent"

@app.task(name='prompt_cron_job')
def prompt_cron_job():
    prompt_detail = PromptDetail()
    prompts = prompt_detail.get_queryset()
    selected_prompts = random.sample(prompts, 2)

    for i, prompt in enumerate(selected_prompts):
        users = User.objects.all()
        for user in users:
            if user.is_admin:
                pass
            else:
                user_token = user.fcm_token[-1]
                if i==0 or i==1:
                    title = prompt.title
                    message = truncate_text(prompt.description, 100) 
                    send_notification(user_token, title, message, notification_type='Prompt Notification')
    
    return "Done"

