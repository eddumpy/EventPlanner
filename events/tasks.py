from django_slack_notifications.utils import send_text

from EventPlanner.celery import app
from events.models import Event


@app.task(name='event_reminder')
def event_reminder(event_id):
    event = Event.objects.filter(pk=int(event_id)).first()
    if event:
        text = event.label + " is starting now."
        send_text(text=text)
