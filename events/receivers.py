from django.dispatch import receiver
from django.db.models.signals import post_save
from events.models import Event
from .tasks import event_reminder
from django_slack_notifications.utils import send_text
from EventPlanner.celery import app


# from django_celery_beat.models import CrontabSchedule, PeriodicTask
# import json


@receiver(post_save, sender=Event)
def event_create_slack_notification(sender, instance, created, **kwargs):
    """Sends a slack notification after an event is created"""

    if created:
        date = instance.start.strftime("%B %d, %Y")
        start_time = instance.start.strftime("%H:%M:%S")
        end_time = instance.end.strftime("%H:%M:%S")
        text = instance.author.first_name + " " + instance.author.last_name + " just created an event \'" \
               + instance.label + "\', that starts on " + date + " at " + start_time \
               + "and ends at " + end_time + "."
        # Sends slack notification
        send_text(text=text)

        # Schedules event reminder when it starts
        event_reminder.apply_async(args=(instance.id,), eta=instance.start)
